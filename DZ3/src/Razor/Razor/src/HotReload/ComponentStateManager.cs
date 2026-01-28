// Licensed to the .NET Foundation under one or more agreements.
// The .NET Foundation licenses this file to you under the MIT license.

using System;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.Linq;
using System.Text.Json;
using System.Text.Json.Serialization;
using Microsoft.AspNetCore.Components;
using Microsoft.Extensions.Logging;

namespace Microsoft.AspNetCore.Razor.HotReload;

/// <summary>
/// Manages component state preservation during hot reload operations.
/// </summary>
public class ComponentStateManager
{
    private readonly ILogger<ComponentStateManager> _logger;
    private readonly ConcurrentDictionary<int, ComponentStateSnapshot> _stateSnapshots = new();
    private readonly ConcurrentDictionary<int, ComponentStateSnapshot> _pendingSnapshots = new();
    private readonly JsonSerializerOptions _jsonOptions;

    /// <summary>
    /// Initializes a new instance of the <see cref="ComponentStateManager"/> class.
    /// </summary>
    /// <param name="logger">The logger for diagnostic information.</param>
    public ComponentStateManager(ILogger<ComponentStateManager> logger)
    {
        _logger = logger ?? throw new ArgumentNullException(nameof(logger));

        _jsonOptions = new JsonSerializerOptions
        {
            PropertyNamingPolicy = JsonNamingPolicy.CamelCase,
            DefaultIgnoreCondition = JsonIgnoreCondition.WhenWritingNull,
            WriteIndented = false
        };
    }

    /// <summary>
    /// Captures the current state of a component for potential restoration during hot reload.
    /// </summary>
    /// <param name="componentState">The component state to capture.</param>
    /// <returns>True if the state was successfully captured; otherwise, false.</returns>
    public bool CaptureState(ComponentState componentState)
    {
        if (componentState == null)
        {
            throw new ArgumentNullException(nameof(componentState));
        }

        try
        {
            var snapshot = CreateSnapshot(componentState);

            if (snapshot != null)
            {
                _pendingSnapshots[componentState.ComponentId] = snapshot;
                _logger.LogDebug("State captured for component {ComponentId}", componentState.ComponentId);
                return true;
            }
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Failed to capture state for component {ComponentId}", componentState.ComponentId);
        }

        return false;
    }

    /// <summary>
    /// Attempts to restore the state of a component from a previously captured snapshot.
    /// </summary>
    /// <param name="componentState">The component state to restore.</param>
    /// <returns>True if the state was successfully restored; otherwise, false.</returns>
    public bool RestoreState(ComponentState componentState)
    {
        if (componentState == null)
        {
            throw new ArgumentNullException(nameof(componentState));
        }

        try
        {
            if (_stateSnapshots.TryGetValue(componentState.ComponentId, out var snapshot))
            {
                var success = ApplySnapshot(componentState, snapshot);

                if (success)
                {
                    _logger.LogDebug("State restored for component {ComponentId}", componentState.ComponentId);
                }
                else
                {
                    _logger.LogWarning("Failed to restore state for component {ComponentId}", componentState.ComponentId);
                }

                return success;
            }
            else
            {
                _logger.LogDebug("No state snapshot found for component {ComponentId}", componentState.ComponentId);
                return false;
            }
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Failed to restore state for component {ComponentId}", componentState.ComponentId);
            return false;
        }
    }

    /// <summary>
    /// Commits pending state snapshots to the main state store.
    /// </summary>
    /// <param name="componentIds">The component IDs to commit.</param>
    public void CommitSnapshots(IEnumerable<int> componentIds)
    {
        if (componentIds == null)
        {
            throw new ArgumentNullException(nameof(componentIds));
        }

        foreach (var componentId in componentIds)
        {
            if (_pendingSnapshots.TryRemove(componentId, out var snapshot))
            {
                _stateSnapshots[componentId] = snapshot;
                _logger.LogDebug("State snapshot committed for component {ComponentId}", componentId);
            }
        }
    }

    /// <summary>
    /// Discards pending state snapshots.
    /// </summary>
    /// <param name="componentIds">The component IDs to discard.</param>
    public void DiscardSnapshots(IEnumerable<int> componentIds)
    {
        if (componentIds == null)
        {
            throw new ArgumentNullException(nameof(componentIds));
        }

        foreach (var componentId in componentIds)
        {
            _pendingSnapshots.TryRemove(componentId, out _);
            _logger.LogDebug("State snapshot discarded for component {ComponentId}", componentId);
        }
    }

    /// <summary>
    /// Clears all stored state snapshots.
    /// </summary>
    public void ClearAllSnapshots()
    {
        var snapshotCount = _stateSnapshots.Count + _pendingSnapshots.Count;

        _stateSnapshots.Clear();
        _pendingSnapshots.Clear();

        _logger.LogInformation("Cleared {SnapshotCount} state snapshots", snapshotCount);
    }

    /// <summary>
    /// Gets the count of stored state snapshots.
    /// </summary>
    public int SnapshotCount => _stateSnapshots.Count + _pendingSnapshots.Count;

    private ComponentStateSnapshot CreateSnapshot(ComponentState componentState)
    {
        try
        {
            // Capture component parameters
            var parameters = CaptureParameters(componentState);

            // Capture render tree if available
            var renderTree = CaptureRenderTree(componentState);

            var snapshot = new ComponentStateSnapshot
            {
                ComponentId = componentState.ComponentId,
                ComponentType = componentState.Component.GetType().AssemblyQualifiedName,
                Parameters = parameters,
                RenderTree = renderTree,
                Timestamp = DateTime.UtcNow,
                Version = 1
            };

            return snapshot;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Failed to create state snapshot for component {ComponentId}", componentState.ComponentId);
            return null;
        }
    }

    private bool ApplySnapshot(ComponentState componentState, ComponentStateSnapshot snapshot)
    {
        try
        {
            if (snapshot.Parameters != null && snapshot.Parameters.Count > 0)
            {
                var parameterView = ParameterView.FromDictionary(snapshot.Parameters);
                componentState.SetDirectParameters(parameterView);
                return true;
            }

            return false;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Failed to apply state snapshot for component {ComponentId}", componentState.ComponentId);
            return false;
        }
    }

    private Dictionary<string, object> CaptureParameters(ComponentState componentState)
    {
        var parameters = new Dictionary<string, object>();

        try
        {
            // This is a simplified parameter capture. In a real implementation,
            // you would need to reflect over the component's properties and
            // capture their current values.

            // For now, we'll capture any parameters that were set via SetParametersAsync
            // This would need to be enhanced based on the actual ComponentState implementation
            return parameters;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Failed to capture parameters for component {ComponentId}", componentState.ComponentId);
            return parameters;
        }
    }

    private string CaptureRenderTree(ComponentState componentState)
    {
        try
        {
            // This is a placeholder for render tree capture
            // In a real implementation, you would serialize the current render tree
            // to preserve the component's visual state

            return null; // For now, we don't capture render tree state
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Failed to capture render tree for component {ComponentId}", componentState.ComponentId);
            return null;
        }
    }
}

/// <summary>
/// Represents a snapshot of component state at a specific point in time.
/// </summary>
public class ComponentStateSnapshot
{
    /// <summary>
    /// Gets or sets the component ID.
    /// </summary>
    public int ComponentId { get; set; }

    /// <summary>
    /// Gets or sets the component type name.
    /// </summary>
    public string ComponentType { get; set; }

    /// <summary>
    /// Gets or sets the component parameters.
    /// </summary>
    public Dictionary<string, object> Parameters { get; set; }

    /// <summary>
    /// Gets or sets the serialized render tree.
    /// </summary>
    public string RenderTree { get; set; }

    /// <summary>
    /// Gets or sets the timestamp when the snapshot was created.
    /// </summary>
    public DateTime Timestamp { get; set; }

    /// <summary>
    /// Gets or sets the snapshot version for compatibility checking.
    /// </summary>
    public int Version { get; set; }
}
