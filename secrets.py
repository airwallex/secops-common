from google.cloud import secretmanager
from secops_common.misc import deserialize, deserialize_str
import os


def read_secret(project_id, secret_name):
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_name}/versions/latest"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data


def read_config(project_id, section):
    section_env = os.environ.get(section)
    if section_env is not None:
        return deserialize_str(section_env)
    else:
        return deserialize(read_secret(project_id, section))
