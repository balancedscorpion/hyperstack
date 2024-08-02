import argparse

from hyperstack import deploy


def main():
    parser = argparse.ArgumentParser(description="Deploy PyTorch or Ollama on Hyperstack")
    subparsers = parser.add_subparsers(dest="command", help="Subcommands")

    # PyTorch subcommand
    pytorch_parser = subparsers.add_parser("pytorch", help="Deploy PyTorch")
    pytorch_parser.add_argument("--name", required=True, help="Name of the virtual machine")
    pytorch_parser.add_argument("--environment", required=True, help="Environment to deploy in")
    pytorch_parser.add_argument("--flavor_name", required=True, help="Flavor name for the VM")
    pytorch_parser.add_argument("--key_name", required=True, help="Name of the key to use")
    pytorch_parser.add_argument(
        "--image_name", default="Ubuntu Server 22.04 LTS R535 CUDA 12.2", help="Name of the image to use"
    )
    pytorch_parser.add_argument("--username", default=None, help="Password of the docker user")
    pytorch_parser.add_argument("--password", default=None, help="Password of the docker user")
    pytorch_parser.add_argument("--docker_image", default=None, help="Docker image to use, if not default")

    # Ollama subcommand
    ollama_parser = subparsers.add_parser("ollama", help="Deploy Ollama")
    ollama_parser.add_argument("--name", required=True, help="Name of the virtual machine")
    ollama_parser.add_argument("--environment", required=True, help="Environment to deploy in")
    ollama_parser.add_argument("--flavor_name", required=True, help="Flavor name for the VM")
    ollama_parser.add_argument("--key_name", required=True, help="Name of the key to use")
    ollama_parser.add_argument(
        "--image_name", default="Ubuntu Server 22.04 LTS R535 CUDA 12.2", help="Name of the image to use"
    )

    args = parser.parse_args()

    if args.command == "pytorch":
        deploy.create_pytorch_vm(
            name=args.name,
            environment=args.environment,
            flavor_name=args.flavor_name,
            key_name=args.key_name,
            image_name=args.image_name,
            username=args.username,
            password=args.password,
            docker_image=args.docker_image,
        )
    elif args.command == "ollama":
        deploy.create_ollama_vm(
            name=args.name,
            environment=args.environment,
            flavor_name=args.flavor_name,
            key_name=args.key_name,
            image_name=args.image_name,
        )
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
