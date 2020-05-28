#!/bin/bash
docker run -itd --name pd_bot -v $(pwd):/app pg_bot
