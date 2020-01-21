#!/usr/bin/env python
# -*- coding: utf-8 -*-
from calendar import month_name
import DB
from datetime import datetime
mes = DB.select('quedadata')
mes = set(mes)
mes
for i in mes:
    print(i[0])




