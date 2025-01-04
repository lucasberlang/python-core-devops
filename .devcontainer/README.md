# Dev Container Python

This project aims to provide a pre-configured development environment for Python using Visual Studio Code with Docker and the Remote - Containers extension. With DevContainer, you can easily set up a consistent development environment across different machines.

## Configuration

### Prerequisites

- Install [Azure SDK](https://azure.microsoft.com/es-es/downloads/)
- Install [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- Install [VS Code Remote Development pack](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack)

### Steps to set up the DevContainer:
1. Clone this repository to your local machine.
2. Open the project in Visual Studio Code.
3. Install the Remote - Containers extension if you haven't already.
4. Click on the "Reopen in Container" button in Visual Studio Code. This will build the DevContainer based on the configuration provided in the `.devcontainer` folder.
5. Once the container is built, you'll have a fully functional development environment ready to use.

### Accessing the DevContainer
- All your project files will be available inside the DevContainer.
- You can access the terminal, install dependencies, and run your code within the container environment.

### Customizing the DevContainer
- You can customize the DevContainer configuration by editing the `.devcontainer/devcontainer.json` file.
- Update the Dockerfile in `.devcontainer/Dockerfile` to add any specific tools or dependencies you need for your project.

### Connecting to Services
- If your project requires connecting to external services like databases, update the necessary configurations in the DevContainer setup to establish the connection.

## Contributing
- Feel free to contribute to this project by opening issues or pull requests.
- Help us improve the DevContainer setup for a better development experience.
