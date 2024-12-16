import docker
import os
import pathlib

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

import pathlib

def run_container(image_name, volume_mount):
    # run docker container
    try:
        client = docker.from_env()
        # container = client.containers.run(image_name, command=command, remove=True)
        mount_path = pathlib.Path(os.getcwd()) / volume_mount

        print(mount_path)
        volume_bindings = { mount_path: { 'bind': '/mount_point', 'mode': 'rw', }, }
        # volume_bindings = { os.getcwd()+"/"+volume_mount: { 'bind': '/sandbox', 'mode': 'rw', }, }
        container = client.containers.run(image_name, volumes=volume_bindings, detach=True)
        # print("Container ran successfully. Output:")
        print(f"Container '{container}' is running...")

        # return container
        # Wait for the container to finish
        exit_status = container.wait()
        if exit_status["StatusCode"] != 0:
            raise RuntimeError(f"Container exited with error: {exit_status}")

        # Extract /tmp/results file from container and extract with get_archive
        output, _ = container.get_archive("/tmp/results")
        dest_path = os.path.join(os.getcwd(), "output.tar")
        with open(dest_path, 'wb') as f:
            for chunk in output:
                f.write(chunk)
                
        # decompress the output
        import tarfile
        with tarfile.open(dest_path, 'r') as tar:
            tar.extractall(path=os.path.join(os.getcwd(), "output"))
        print(f"Output saved to {os.path.join(os.getcwd(), 'output')}")
        
        # read the output
        output = []
        for root, _, files in os.walk(os.path.join(os.getcwd(), "output")):
            for file in files:
                with open(os.path.join(root, file), 'r') as f:
                    output.append(f.read())
        
        # delete the output
        os.remove(dest_path)
        import shutil
        shutil.rmtree(os.path.join(os.getcwd(), "output"))
        
        # print(f"Output: {output}")        
        return output
    except Exception as e:
        print(f"Error during Docker run: {e}")
        return 1
    
    # finally:
    #     # Cleanup container and context
    #     if container:
    #         container.remove(force=True)


if __name__ == "__main__":
    image_name = "sandbox-container"
    context_path = "sandbox/benchmarker"
    executable = "mount_point"
    build_container(image_name, context_path)
    run_container(image_name=image_name, volume_mount=f"/{context_path}/{executable}")

# sandbox_folders = os.listdir(context_path)
# for folder_name in sandbox_folders:
#     image_name = build_container(folder_name, context_path + '/' + folder_name + "/Dockerfile")
#     run_container(image_name, command)