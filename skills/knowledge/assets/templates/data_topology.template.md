# Data Topology & File Locations

[[index|← Back to MOC]]

## Verified Repository & Runtime Paths

| Category | Path | Lifecycle / Mutability | Notes |
| :--- | :--- | :--- | :--- |
| **Active Config** | `{{CONFIG_PATH}}` | Immutable at runtime | Primary system parameters |
| **Execution Runs** | `{{RUNS_PATH}}` | Mutable runtime outputs | Execution outputs & journals |
| **System Logs** | `{{LOGS_PATH}}` | Append-only logs | Diagnostics and trace logs |
| **Telemetry / Reports** | `{{REPORTS_PATH}}` | Generated post-run | Performance reports & metrics |
| **Data Lake / Fixtures** | `{{DATA_PATH}}` | Read-only input data | Source datasets or fixtures |
| **Isolated Test Temp** | `{{TEST_TMP_PATH}}` | Disposable | Test scratch directories |
