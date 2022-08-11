""" Common bigtable infra"""

from google.cloud import bigquery

from secops_common.logsetup import logger

from google.api_core.exceptions import NotFound

import time

bigquery_client = bigquery.Client()

schema = {}

dataset = ''
project = ''


def assert_environment():
    assert dataset != ''
    assert project != ''

def get_dataset():
    dataset_ref = bigquery_client.dataset(dataset)
    return bigquery_client.get_dataset(dataset_ref)


def get_table(name):
    try:
        dataset_ref = get_dataset()
        table_ref = dataset_ref.table(name)
        return bigquery_client.get_table(table_ref)
    except NotFound as e:
        create_table(name)
        create_view(name)
        logger.info(f'waiting 10s for table {name} to be ready')
        time.sleep(10)
        return bigquery_client.get_table(table_ref)


def create_table(name):
    _schema = schema[name]
    dataset_ref = get_dataset()
    table_ref = dataset_ref.table(name)
    table = bigquery.Table(table_ref, schema=_schema)
    table = bigquery_client.create_table(table)
    logger.info('table {} created.'.format(table.table_id))


""" Create a read only view with latest records (by create_at timestamp) """
def create_view(name):
    assert_environment()
    id_col = schema[name][0].name
    client = bigquery.Client()
    view_id = f"{project}.{dataset}.{name}_latest"
    view = bigquery.Table(view_id)
    view.view_query = f"SELECT  *  FROM `{project}.{dataset}.{name}` WHERE created_at = (SELECT MAX(created_at) FROM `{project}.{dataset}.{name}`)"

    view = client.create_table(view)
    logger.info(f"Created {view_id} view table for {name}")


def insert_rows(rows, name):
    table = get_table(name)
    errors = bigquery_client.insert_rows(table, rows)
    if (len(errors) > 0):
        for error in errors:
            logger.error(error)

    assert errors == []


def run_query(q):
    query_job = bigquery_client.query(q)
    return query_job.result()


def delete_table_and_view(name):
    assert_environment()
    view = f'{project}.{dataset}.{name}_latest'
    table = f'{project}.{dataset}.{name}'
    bigquery_client.delete_table(table, not_found_ok=True)
    bigquery_client.delete_table(view, not_found_ok=True)
    logger.info(f'table {name} deleted')


def latest_rows(table):
    q = f'SELECT * from {project}.{dataset}.{table}_latest'
    return run_query(q)
