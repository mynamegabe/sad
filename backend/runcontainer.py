import docker
import os




def build_container(image_name, context_path):
    # build docker container
    try:
        client = docker.from_env()
        image, logs = client.images.build(path=context_path, tag=image_name, rm=True)
        # for log in logs:
        #     if "stream" in log:
        #         print(log["stream"].strip())
        print(image)
        print(f"Image '{image_name}' built successfully.")
        return image_name
    except docker.errors.BuildError as e:
        print(f"Error during Docker build: {e}")
        return 1

def run_container(image_name, command):
    # run docker container
    try:
        client = docker.from_env()
        # container = client.containers.run(image_name, command=command, remove=True)
        volume_bindings = { 'sandbox/mount_point': { 'bind': '/app', 'mode': 'rwx', }, }
        container = client.containers.run(image_name, volumes=volumes, detach=True)
        print("Container ran successfully. Output:")
        print(f"Container '{container}' is running...")

        return container
        # # Wait for the container to finish
        # exit_status = container.wait()
        # if exit_status["StatusCode"] != 0:
        #     raise RuntimeError(f"Container exited with error: {exit_status}")

        # # Copy the /tmp/output file from the container
        # output_archive = container.get_archive("/tmp/output")
        # output_tar_data, _ = output_archive

        # # Extract file content from the tar archive
        # import tarfile
        # import io

        # with tarfile.open(fileobj=io.BytesIO(output_tar_data)) as tar:
        #     for member in tar.getmembers():
        #         if member.name == "output":  # Extract the desired file
        #             file_data = tar.extractfile(member).read()
        #             print("Content of /tmp/output:")
        #             print(file_data.decode())
        #             break
    except docker.errors.ContainerError as e:
        print(f"Error running container: {e}")
    except docker.errors.ImageNotFound as e:
        print(f"Image not found: {e}")
    except docker.errors.APIError as e:
        print(f"API error: {e}")
    # finally:
    #     # Cleanup container and context
    #     if container:
    #         container.remove(force=True)


image_name = "sandbox-container"
context_path = "sandbox/benchmarker"
executable = "ls_mainexe"
build_container(image_name, context_path)
run_container(image_name=image_name, command=executable)

# sandbox_folders = os.listdir(context_path)
# for folder_name in sandbox_folders:
#     image_name = build_container(folder_name, context_path + '/' + folder_name + "/Dockerfile")
#     run_container(image_name, command)