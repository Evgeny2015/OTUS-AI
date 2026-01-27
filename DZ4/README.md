* llm: ollama (llama3.2:3b)
* web API [readme](./backend/README.md)
```sh
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# run
python app.py
```
* agent [readme](./agent/README.md)
```sh
# use only python 3.13.11 !!!
cd agent
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

#run
python langchain_agent.py
```

# prompts
## #1
```
You: get users
```

> Entering new AgentExecutor chain...

Invoking: `get_all_users` with `{}`


ToolResponse(status='success', action='get_all_users', data={'users': [{'created_at': '2026-01-25T18:01:41.071590', 'email': 'alice.updated@example.com', 'id': 1, 'updated_at': '2026-01-27T16:11:21.362861', 'username': 'john_doe'}, {'created_at': '2026-01-27T16:09:41.729573', 'email': 'bob@example.com', 'id': 3, 'updated_at': '2026-01-27T16:09:41.729580', 'username': 'Bob'}], 'count': 2, 'message': 'Retrieved 2 users'})Here are the users:

1. username: john_doe, email: alice.updated@example.com
2. username: Bob, email: bob@example.com

> Finished chain.
```
Agent: Here are the users:

1. username: john_doe, email: alice.updated@example.com
2. username: Bob, email: bob@example.com
```

## #2
```
You: Create a user named Admin with email admin@example.com
```

> Entering new AgentExecutor chain...

Invoking: `create_user` with `{'username': 'Admin', 'email': 'admin@example.com'}`


ToolResponse(status='success', action='create_user', data={'user': {'created_at': '2026-01-27T18:23:17.828050', 'email': 'admin@example.com', 'id': 4, 'updated_at': '2026-01-27T18:23:17.828099', 'username': 'Admin'}, 'message': 'Successfully created user: Admin'})The user "Admin" with email "admin@example.com" has been successfully created.

> Finished chain.
```
Agent: The user "Admin" with email "admin@example.com" has been successfully created.
```

## #3
```
You: get users
```

> Entering new AgentExecutor chain...

Invoking: `get_all_users` with `{}`


ToolResponse(status='success', action='get_all_users', data={'users': [{'created_at': '2026-01-25T18:01:41.071590', 'email': 'alice.updated@example.com', 'id': 1, 'updated_at': '2026-01-27T16:11:21.362861', 'username': 'john_doe'}, {'created_at': '2026-01-27T16:09:41.729573', 'email': 'bob@example.com', 'id': 3, 'updated_at': '2026-01-27T16:09:41.729580', 'username': 'Bob'}, {'created_at': '2026-01-27T18:23:17.828050', 'email': 'admin@example.com', 'id': 4, 'updated_at': '2026-01-27T18:23:17.828099', 'username': 'Admin'}], 'count': 3, 'message': 'Retrieved 3 users'})Here are the users:

1. id: 1
   username: john_doe
   email: alice.updated@example.com
   created_at: 2026-01-25T18:01:41.071590
   updated_at: 2026-01-27T16:11:21.362861

2. id: 3
   username: Bob
   email: bob@example.com
   created_at: 2026-01-27T16:09:41.729573
   updated_at: 2026-01-27T16:09:41.729580

3. id: 4
   username: Admin
   email: admin@example.com
   created_at: 2026-01-27T18:23:17.828050
   updated_at: 2026-01-27T18:23:17.828099

> Finished chain.
```
Agent: Here are the users:

1. id: 1
   username: john_doe
   email: alice.updated@example.com
   created_at: 2026-01-25T18:01:41.071590
   updated_at: 2026-01-27T16:11:21.362861

2. id: 3
   username: Bob
   email: bob@example.com
   created_at: 2026-01-27T16:09:41.729573
   updated_at: 2026-01-27T16:09:41.729580

3. id: 4
   username: Admin
   email: admin@example.com
   created_at: 2026-01-27T18:23:17.828050
   updated_at: 2026-01-27T18:23:17.828099
```
## #4
```
You: delete user 1
```

> Entering new AgentExecutor chain...

Invoking: `delete_user` with `{'user_id': '1'}`


ToolResponse(status='success', action='delete_user', data={'user_id': '1', 'message': 'Successfully deleted user 1'})User 1 has been successfully deleted.

> Finished chain.
```
Agent: User 1 has been successfully deleted.
```

## #5
```
You: Update user 4's email to admin.updated@example.com
```

> Entering new AgentExecutor chain...

Invoking: `update_user` with `{'user_id': '4', 'email': 'admin.updated@example.com'}`


ToolResponse(status='success', action='update_user', data={'user': {'created_at': '2026-01-27T18:23:17.828050', 'email': 'admin.updated@example.com', 'id': 4, 'updated_at': '2026-01-27T18:29:31.671850', 'username': 'Admin'}, 'message': 'Successfully updated user 4'})User 4's email has been successfully updated to admin.updated@example.com.

> Finished chain.
```
Agent: User 4's email has been successfully updated to admin.updated@example.com.
```

## #6
```
You: get users
```

> Entering new AgentExecutor chain...

Invoking: `get_all_users` with `{}`


ToolResponse(status='success', action='get_all_users', data={'users': [{'created_at': '2026-01-27T16:09:41.729573', 'email': 'bob@example.com', 'id': 3, 'updated_at': '2026-01-27T16:09:41.729580', 'username': 'Bob'}, {'created_at': '2026-01-27T18:23:17.828050', 'email': 'admin.updated@example.com', 'id': 4, 'updated_at': '2026-01-27T18:29:31.671850', 'username': 'Admin'}], 'count': 2, 'message': 'Retrieved 2 users'})Here are the users retrieved from the system:

1. Bob (id=3) - bob@example.com
2. Admin (id=4) - admin.updated@example.com

> Finished chain.
```
Agent: Here are the users retrieved from the system:

1. Bob (id=3) - bob@example.com
2. Admin (id=4) - admin.updated@example.com
```