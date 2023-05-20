from flask import Flask, render_template, url_for, request, jsonify, redirect, send_file, send_from_directory
import threading, json, os, requests, datetime, time

if __name__ == '__main__':
    url = requests.get(
                'http://localhost/api?action=delete_model&webs=mfc&model_username=SexyNicolle29')
    print(url)