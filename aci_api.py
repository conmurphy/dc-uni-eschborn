'''Copyright (c) 2019 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.0 (the "License"). You may obtain a copy of the
License at
               https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.'''



import json
import os
import requests

from tabulate import tabulate

import acitoolkit.acitoolkit as ACI
from acitoolkit.aciphysobject import * 

from dcUniConfig import config

ACI_URL = config.ACI_URL
ACI_USER = config.ACI_USER
ACI_PASSWORD = config.ACI_PASSWORD


def aciGetTenants(session):
    
    tenants = ACI.Tenant.get(session)
    
    print("newBranch")
    
    output = []
    
    for tenant in tenants:
        apps = ACI.AppProfile.get(session, tenant)
        for app in apps:
            epgs = ACI.EPG.get(session, app, tenant)
            for epg in epgs:
                tenantName = ""
                appName = ""
                if not any(tenant.name in f for f in output):
                    tenantName = tenant.name
                if not any(app.name in f for f in output):
                    appName = app.name
                output.append([tenantName,appName,epg.name])

    print ("\n")
    print(tabulate(output, headers=["Tenant Name","App Name","EPG Name"]))

def aciGetContracts(session):
    
    tenants = ACI.Tenant.get(session)

    output = []

    for tenant in tenants:
        contracts = ACI.Contract.get(session,tenant)
    
        for contract in contracts:
            tenantName = ""
            if not any(tenant.name in f for f in output):
                tenantName = tenant.name
            output.append([tenantName,contract.name,contract._scope])

    print ("\n")
    print(tabulate(output, headers=["Tenant Name","Contract Name","Scope"]))

def aciGetNodes(session):

    nodes = Node.get(session)

    output = []
    for node in nodes:
        output.append([node.node,node.name,node.role,node.model,node.oper_st,node.serial,node.firmware,node.ipAddress])
    
    print ("\n")
    print(tabulate(output, headers=["ID","Node Name","Role","Model","State","Serial","Firmware","IP Address"]))

if __name__ == '__main__':
    session = Session("https://{}".format(ACI_URL), ACI_USER, ACI_PASSWORD)
    session.login()
    aciGetTenants(session)
    aciGetContracts(session)
    aciGetNodes(session)


