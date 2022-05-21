from typing import List, Optional

from ruamel.yaml import YAML

from compose_viz.compose import Compose, Service
from compose_viz.extends import Extends

class Parser:
    def __init__(self):
        pass

    def parse(self, file_path: str) -> Compose:
        # load the yaml file
        with open(file_path, "r") as f:
            try:
                yaml = YAML(typ="safe", pure=True)
                yaml_data = yaml.load(f)
            except Exception as e:
                raise RuntimeError(f"Error parsing file '{file_path}': {e}")

        # validate the yaml file
        if not yaml_data:
            raise RuntimeError("Empty yaml file, aborting.")

        if not yaml_data.get("services"):
            raise RuntimeError("No services found, aborting.")

        # parse services data into Service objects
        services_data = yaml_data["services"]
        services = []

        for service, service_name in zip(services_data.values(), services_data.keys()):
            print("name: {}".format(service_name))

            service_image: Optional[str] = None
            if service.get("image"):
                service_image = service["image"]
                print("image: {}".format(service_image))

            service_networks: List[str] = []
            if service.get("networks"):
                if type(service["networks"]) is list:
                    service_networks = service["networks"]
                else:
                    service_networks = list(service["networks"].keys())
                print("networks: {}".format(service_networks))
            
            service_image: Optional[str] = None
            if service.get("image"):
                service_image = service["image"]
                print("image: {}".format(service_image))

            service_extends: Optional[Extends] = None
            if service.get("extends"):
                service_extends = Extends(service_name=service["extends"]["service"])
                print("extends: {}".format(service_extends))
            

            services.append(
                Service(
                    name=service_name,
                    image=service_image,
                    networks=service_networks,
                    extends=service_extends
                )
            )

        # create Compose object
        compose = Compose(services)

        return compose
