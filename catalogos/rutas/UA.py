from .rutas import catalogos
from flask import render_template, request, jsonify

from catalogos.modelos.modelos import Kua
from app import db
