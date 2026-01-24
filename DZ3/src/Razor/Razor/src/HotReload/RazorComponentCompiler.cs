// Licensed to the .NET Foundation under one or more agreements.
// The .NET Foundation licenses this file to you under the MIT license.

using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Razor.Language;
using Microsoft.AspNetCore.Razor.Language.CodeGeneration;
using Microsoft.CodeAnalysis;
using Microsoft.CodeAnalysis.CSharp;
using Microsoft.Extensions.Logging;

namespace Microsoft.AspNetCore.Razor.HotReload;

/// <summary>
/// Handles recompilation of Razor components during hot reload.
/// </summary>
public class RazorComponentCompiler
{
    private readonly ILogger<RazorComponentCompiler> _logger;
    private readonly Dictionary<string, CompilationResult> _compilationCache = new Dictionary<string, CompilationResult>(StringComparer.OrdinalIgnoreCase);
    private readonly object _cacheLock = new object();

    /// <summary>
    /// Initializes a new instance of the <see cref="RazorComponentCompiler"/> class.
    /// </summary>
    /// <param name="logger">The logger for diagnostic information.</param>
    public RazorComponentCompiler(ILogger<RazorComponentCompiler> logger)
    {
        _logger = logger ?? throw new ArgumentNullException(nameof(logger));
    }

    /// <summary>
    /// Recompiles a Razor component from the specified file path.
    /// </summary>
    /// <param name="componentPath">The path to the .razor file to recompile.</param>
    /// <returns>A <see cref="CompilationResult"/> containing the compilation outcome.</returns>
    public async Task<CompilationResult> RecompileComponentAsync(string componentPath)
    {
        if (string.IsNullOrEmpty(componentPath))
        {
            throw new ArgumentException("Component path cannot be null or empty.", nameof(componentPath));
        }

        if (!File.Exists(componentPath))
        {
            throw new FileNotFoundException($"Component file not found: {componentPath}", componentPath);
        }

        var stopwatch = Stopwatch.StartNew();

        try
        {
            _logger.LogInformation("Starting recompilation of component: {ComponentPath}", componentPath);

            // Parse Razor syntax
            var syntaxTree = await ParseRazorSyntaxAsync(componentPath);
            if (syntaxTree.Diagnostics.Any(d => d.Severity == RazorDiagnosticSeverity.Error))
            {
                return CompilationResult.Failure(componentPath, syntaxTree.Diagnostics);
            }

            // Generate C# code
            var generatedCode = GenerateCSharpCode(syntaxTree);
            if (string.IsNullOrEmpty(generatedCode))
            {
                return CompilationResult.Failure(componentPath, new[] { CreateErrorDiagnostic("Failed to generate C# code") });
            }

            // Compile to assembly
            var compilationResult = await CompileToAssemblyAsync(generatedCode, componentPath);

            stopwatch.Stop();

            if (compilationResult.Success)
            {
                _logger.LogInformation("Component recompiled successfully in {Duration}ms: {ComponentPath}",
                    stopwatch.ElapsedMilliseconds, componentPath);

                // Cache successful compilation
                lock (_cacheLock)
                {
                    _compilationCache[componentPath] = compilationResult;
                }
            }
            else
            {
                _logger.LogWarning("Component compilation failed after {Duration}ms: {ComponentPath}",
                    stopwatch.ElapsedMilliseconds, componentPath);
            }

            return compilationResult;
        }
        catch (Exception ex)
        {
            stopwatch.Stop();
            _logger.LogError(ex, "Failed to recompile component in {Duration}ms: {ComponentPath}",
                stopwatch.ElapsedMilliseconds, componentPath);

            return CompilationResult.Failure(componentPath, new[] { CreateErrorDiagnostic(ex.Message) });
        }
    }

    /// <summary>
    /// Gets a cached compilation result if available.
    /// </summary>
    /// <param name="componentPath">The path to the component.</param>
    /// <returns>The cached compilation result, or null if not cached.</returns>
    public CompilationResult GetCachedResult(string componentPath)
    {
        lock (_cacheLock)
        {
            return _compilationCache.TryGetValue(componentPath, out var result) ? result : null;
        }
    }

    /// <summary>
    /// Clears the compilation cache.
    /// </summary>
    public void ClearCache()
    {
        lock (_cacheLock)
        {
            _compilationCache.Clear();
        }
        _logger.LogInformation("Compilation cache cleared");
    }

    private async Task<RazorSyntaxTree> ParseRazorSyntaxAsync(string componentPath)
    {
        var source = RazorSourceDocument.ReadFrom(componentPath);
        var engine = RazorProjectEngine.Create(RazorConfiguration.Default, RazorProjectFileSystem.Empty);

        var codeDocument = engine.Process(source);
        return codeDocument.GetSyntaxTree();
    }

    private string GenerateCSharpCode(RazorSyntaxTree syntaxTree)
    {
        try
        {
            var engine = RazorProjectEngine.Create(RazorConfiguration.Default, RazorProjectFileSystem.Empty);
            var codeDocument = engine.Process(syntaxTree.Source);

            var csharpDocument = codeDocument.GetCSharpDocument();
            return csharpDocument.GeneratedCode;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Failed to generate C# code from syntax tree");
            return null;
        }
    }

    private async Task<CompilationResult> CompileToAssemblyAsync(string generatedCode, string componentPath)
    {
        try
        {
            var compilation = CreateCompilation(generatedCode, componentPath);
            var emitResult = compilation.Emit();

            if (emitResult.Success)
            {
                var assemblyBytes = emitResult.GetAssemblyImage();
                var assembly = Assembly.Load(assemblyBytes);

                return CompilationResult.Success(componentPath, assembly, generatedCode);
            }
            else
            {
                var diagnostics = emitResult.Diagnostics
                    .Where(d => d.Severity == DiagnosticSeverity.Error)
                    .Select(d => CreateErrorDiagnostic($"{d.Id}: {d.GetMessage()}"))
                    .ToArray();

                return CompilationResult.Failure(componentPath, diagnostics);
            }
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Failed to compile generated C# code");
            return CompilationResult.Failure(componentPath, new[] { CreateErrorDiagnostic(ex.Message) });
        }
    }

    private CSharpCompilation CreateCompilation(string generatedCode, string componentPath)
    {
        var syntaxTree = CSharpSyntaxTree.ParseText(generatedCode);

        var references = GetCompilationReferences();

        var assemblyName = Path.GetFileNameWithoutExtension(componentPath) + "_HotReload";

        return CSharpCompilation.Create(
            assemblyName,
            new[] { syntaxTree },
            references,
            new CSharpCompilationOptions(
                OutputKind.DynamicallyLinkedLibrary,
                optimizationLevel: OptimizationLevel.Debug,
                allowUnsafe: true));
    }

    private IEnumerable<MetadataReference> GetCompilationReferences()
    {
        // Add references to required assemblies
        var references = new List<MetadataReference>
        {
            MetadataReference.CreateFromFile(typeof(object).Assembly.Location),
            MetadataReference.CreateFromFile(typeof(ComponentBase).Assembly.Location),
            MetadataReference.CreateFromFile(typeof(RazorPageBase).Assembly.Location),
        };

        // Add additional references as needed
        var additionalAssemblies = new[]
        {
            "Microsoft.AspNetCore.Components",
            "Microsoft.AspNetCore.Components.Web",
            "Microsoft.AspNetCore.Razor",
            "Microsoft.Extensions.Logging.Abstractions"
        };

        foreach (var assemblyName in additionalAssemblies)
        {
            try
            {
                var assembly = Assembly.Load(new AssemblyName(assemblyName));
                references.Add(MetadataReference.CreateFromFile(assembly.Location));
            }
            catch (Exception ex)
            {
                _logger.LogWarning(ex, "Failed to load assembly reference: {AssemblyName}", assemblyName);
            }
        }

        return references;
    }

    private RazorDiagnostic CreateErrorDiagnostic(string message)
    {
        return RazorDiagnostic.Create(
            new RazorDiagnosticDescriptor("RCH0001", () => message, RazorDiagnosticSeverity.Error),
            RazorSourceSpan.Undefined);
    }
}

/// <summary>
/// Represents the result of a component compilation operation.
/// </summary>
public class CompilationResult
{
    /// <summary>
    /// Gets a value indicating whether the compilation was successful.
    /// </summary>
    public bool Success { get; }

    /// <summary>
    /// Gets the path to the component that was compiled.
    /// </summary>
    public string ComponentPath { get; }

    /// <summary>
    /// Gets the compiled assembly, if compilation was successful.
    /// </summary>
    public Assembly CompiledAssembly { get; }

    /// <summary>
    /// Gets the generated C# code.
    /// </summary>
    public string GeneratedCode { get; }

    /// <summary>
    /// Gets any diagnostics produced during compilation.
    /// </summary>
    public IReadOnlyList<RazorDiagnostic> Diagnostics { get; }

    private CompilationResult(bool success, string componentPath, Assembly compiledAssembly, string generatedCode, IReadOnlyList<RazorDiagnostic> diagnostics)
    {
        Success = success;
        ComponentPath = componentPath;
        CompiledAssembly = compiledAssembly;
        GeneratedCode = generatedCode;
        Diagnostics = diagnostics;
    }

    /// <summary>
    /// Creates a successful compilation result.
    /// </summary>
    /// <param name="componentPath">The path to the component.</param>
    /// <param name="compiledAssembly">The compiled assembly.</param>
    /// <param name="generatedCode">The generated C# code.</param>
    /// <returns>A successful compilation result.</returns>
    public static CompilationResult Success(string componentPath, Assembly compiledAssembly, string generatedCode)
    {
        return new CompilationResult(true, componentPath, compiledAssembly, generatedCode, Array.Empty<RazorDiagnostic>());
    }

    /// <summary>
    /// Creates a failed compilation result.
    /// </summary>
    /// <param name="componentPath">The path to the component.</param>
    /// <param name="diagnostics">The compilation diagnostics.</param>
    /// <returns>A failed compilation result.</returns>
    public static CompilationResult Failure(string componentPath, IReadOnlyList<RazorDiagnostic> diagnostics)
    {
        return new CompilationResult(false, componentPath, null, null, diagnostics);
    }
}
