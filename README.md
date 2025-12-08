# Gym-Membership-System

A lightweight, interactive, and extendable SQLite + Streamlit application for managing gym members, memberships, classes, phone records, and more.

## Overview

This project provides a simple but powerful management interface built with Streamlit and SQLite3.

**Key Features:**
* 📋 **View Tables:** Browse all database records instantly.
* ➕ **Insert Data:** Register new members, trainers, and classes via forms.
* 🔄 **Update & Delete:** Modify or remove existing records easily.
* 🔗 **Complex Queries:** Perform JOIN operations to analyze membership trends.
* 🐳 **Dockerized:** Runs smoothly in a containerized environment.

## Prerequisites

Before running the project, make sure your system meets the following requirements:

1. **Docker Desktop installed** - Provides the Docker CLI and Docker Engine.
2. **Virtualization enabled** (Intel VT-x / AMD-V)
   - Required to run Linux-based containers.
3. **WSL2 enabled** (for Windows Home users)
   - Docker uses a lightweight Linux kernel under the hood.
4. **Make** (Optional but highly recommended)
   - A build automation tool to simplify running commands.
   - *Windows users:* Can install via Chocolatey (`choco install make`) or use inside WSL.
   - *Linux/Mac users:* Usually pre-installed.

Without these prerequisites, the application may not start correctly.

---

## Quick Start

We have included a `Makefile` to simplify common Docker tasks. You don't need to memorize long Docker commands! This file acts as a control center for the project.

### 1. View Help Menu
If you are unsure which command to run, list all available shortcuts directly in your terminal.
```bash
make
# OR
make info
```

### 2. Build the Docker Image
Before running the application, build the Docker image from the Dockerfile.
```bash
make build
```

### 3. Start the Application
Run the application in the background (detached mode).
```bash
make up
```
Once started, the application will be available at: **http://localhost:8501**

### 4. View Live Logs
To monitor what's happening in the container in real-time:
```bash
make logs
```
This is useful for debugging and tracking application events.

### 5. Stop the Application
When you're done, stop and remove the running containers:
```bash
make down
```

### 6. Clean Up Docker Resources
To remove unused Docker images, containers, and networks (to save disk space):
```bash
make clean
```
**Warning:** This will delete unused objects. Use with caution.

---

## Makefile Commands Summary

| Command | Description |
|---------|-------------|
| `make info` | Display all available commands |
| `make build` | Build the Docker image |
| `make up` | Start the application (background) |
| `make down` | Stop and remove containers |
| `make logs` | View live container logs |
| `make clean` | Prune unused Docker objects |

---

## Project Structure

```
Gym-Membership-System/
├── app/
│   ├── app.py
│   ├── database.py
│   ├── insertion.py
│   ├── queries.py
│   ├── update.py
│   ├── delete.py
│   ├── insert_data.py
│   └── insertion.py
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── requirements.txt
└── README.md
```

---

## Support & Troubleshooting

If you encounter any issues:
1. Ensure Docker Desktop is running
2. Check that port 8501 is not in use
3. Run `make logs` to see detailed error messages
4. Verify that all prerequisites are installed
