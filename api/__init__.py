from flask import Flask
from flask_cors import  *
from py2neo import Graph

# 创建项目对象
APP = Flask(__name__)
# 加载配置文件内容
APP.config.from_object('api.setting')
APP.config.from_envvar('FLASK_SETTING')

#创建neo4j数据库对象
DB = Graph(
        
    )
CORS(APP, suports_credential=True)

from api.model import Node
from api.controller import program_handler