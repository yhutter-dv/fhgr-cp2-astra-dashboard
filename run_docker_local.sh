#!/bin/bash
sudo docker compose --env-file backend/.env-local up -d --build
