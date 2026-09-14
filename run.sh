#!/bin/bash
bash download_ebooks.sh
gunicorn wsgi:app
