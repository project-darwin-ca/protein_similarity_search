import streamlit as st
import py3Dmol
from stmol import showmol
from snowflake.snowpark import Session
import requests
import pandas as pd
import json
import os
import snowflake.connector
from snowflake.snowpark.functions import col


# Environment Variables

def connection() -> snowflake.connector.SnowflakeConnection:
  if os.path.isfile("/snowflake/session/token"):
      creds = {
          'host': os.getenv('SNOWFLAKE_HOST'),
          'port': os.getenv('SNOWFLAKE_PORT'),
          'protocol': "https",
          'account': os.getenv('SNOWFLAKE_ACCOUNT'),
          'authenticator': "oauth",
          'token': open('/snowflake/session/token', 'r').read(),
          'warehouse': os.getenv('SNOWFLAKE_WAREHOUSE'),
          'database': os.getenv('SNOWFLAKE_DATABASE'),
          'schema': os.getenv('SNOWFLAKE_SCHEMA'),
          'client_session_keep_alive': True
      }
  else:
      creds = {
          'account': os.getenv('SNOWFLAKE_ACCOUNT'),
          'user': os.getenv('SNOWFLAKE_USER'),
          'password': os.getenv('SNOWFLAKE_PASSWORD'),
          'warehouse': os.getenv('SNOWFLAKE_WAREHOUSE'),
          'database': os.getenv('SNOWFLAKE_DATABASE'),
          'schema': os.getenv('SNOWFLAKE_SCHEMA'),
          'client_session_keep_alive': True
      }
    
  connection = snowflake.connector.connect(**creds)
  return connection

def setupsession() -> Session:
    return Session.builder.configs({"connection": connection()}).create()

# Setup a Snowflake session
session = setupsession()

def find_nth(haystack, needle, n):
     parts = haystack.split(needle, n+1)
     if len(parts)<=n+1:
         return -1
     return len(haystack)-len(parts[-1])-len(needle)

# Pull protein information from Uniprot
def get_desc(id):
