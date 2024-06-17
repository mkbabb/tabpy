# `tabpy`

Dockerized 🐳 implementation of a TabPy server.

## What's TabPy?

TabPy is a Python server that lets you execute Python code on the fly and display results in Tableau visualizations. For more information, visit the [official documentation](https://tableau.github.io/TabPy/) or the official [GitHub repository](https://github.com/tableau/TabPy).

## Usage

We use [`poetry`](https://python-poetry.org/) to manage the Python dependencies in conjunction with `docker-compose` to manage the Docker services.

Execute the following command to build and run the Docker services:

```bash
docker compose down && docker compose up -d --build
```

-   `docker compose down` stops and removes the Docker services.
-   `docker compose up -d --build` builds and runs the Docker services in the background, ensuring it runs on system startup.

The TabPy container is exposed on port `8001` at `http://localhost:8001/`. Proxying to a web server is recommended.

The TabPy password management system is **enabled** by default (this is necessary for Tableau Online and Tableau Server).

## TabPy Information

### Users

Manage TabPy user accounts using the `tabpy-user` command-line utility.

#### Configuring TabPy with Authentication

Configure TabPy to use the passwords file for authentication. Create a configuration file (`tabpy_auth.conf`):

```ini
[TabPy]
TABPY_PWD_FILE = <path_to_password_file>
```

#### Adding a User

```bash
tabpy-user add -u <username> -f <path_to_password_file> -p <password>
```

#### Updating a User Password

```bash
tabpy-user update -u <username> -f <path_to_password_file> -p <new_password>
```

#### Deleting a User

Manually delete the user's line in the passwords file.

### Tableau Configuration

#### Tableau Desktop

1. Go to **Help** > **Settings and Performance** > **Manage External Service Connection**.
2. Set connection type to **TabPy/External API**.
3. Enter **Server (host)** and **Port**.
4. Check **Sign with username and password** and enter credentials.
5. Click **Test Connection**.

#### Tableau Prep

TODO

#### Tableau Public

**TabPy is not supported in Tableau Public.**

#### Tableau Online

TODO

#### Tableau Server

TODO

## Scripts

Several scripts are available to test out the TabPy server:

### [`./src/nodes.py`](nodes.py)

Implementation of a live, and fairly performant, graph visualization using the `networkx` library. The script generates the `x`, `y`, and `weight` attributes for each node and edge in the graph.

### [`./src/explode_week_range`](explode_week_range.py)

This script, meant for Tableau Prep, takes the `Week #` column and explodes it into a range of weeks. For example, one row with `1-3` will be exploded into three rows: `1`, `2`, and `3` & c.

### [`./src/radar.py`](radar.py)

Poor-mans implementation of a radar chart using edge bundling. The script generates the `x`, `y`, and `weight` attributes for each node and edge in the graph.
