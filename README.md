# Gym-Membership-System

A lightweight, interactive, and extendable SQLite + Streamlit application for managing gym members, memberships, classes, phone records, and more.

## Overview

This project provides a simple but powerful management interface built with Streamlit and SQLite3.

You can:

* View all tables in the database
*Insert new records
* Update existing data
* Delete entries
* Perform JOIN operations to see combined membership & class data
* The interface is user-friendly and runs entirely in your browser.

## Prerequisites

Before running the project with Docker, make sure your system meets the following requirements:

1. Docker Desktop installed  
   - Provides the Docker CLI and Docker Engine

2. Virtualization enabled (Intel VT-x / AMD-V)
   - Required to run Linux-based containers

3. WSL2 enabled (for Windows Home users)
   - Docker uses a lightweight Linux kernel under the hood

4. 64-bit CPU + minimum 4GB RAM
   - Ensures stable container performance

Without these prerequisites, Docker containers cannot start.


## 🐳 Run with Docker

You can run the app fully containerized using Docker.

```bash
docker compose up --build
```

