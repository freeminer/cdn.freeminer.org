#!/bin/bash
uwsgi -s /tmp/cdn.freeminer.org.sock -w main:app --chmod-socket=777 -p 15 --threads 1
