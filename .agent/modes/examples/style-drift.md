# Style Drift Full Example

Read this file only when the compact card is insufficient, when the user explicitly asks for a full example for this risk, or when this exact failure mode remains ambiguous.

User request: "Add logging to the upload function."

Wrong pattern:

```diff
- def upload_file(file_path, destination):
+ def upload_file(file_path: str, destination: str) -> bool:
+     """Upload file to destination with logging."""
```

Problems:

- Adds type hints nobody requested.
- Adds a docstring where the local file may not use them.
- Risks changing style and public expectations while adding logging.

Better pattern:

```diff
+ logger.info(f'Starting upload: {file_path}')
  try:
      ...
+     logger.info(f'Upload successful: {file_path}')
```

Preserve local style and change only what is needed for logging.
