import os


def block_hosts_ingress(hosts):
    hosts_string = ",".join(hosts)
    cmd = "kubectl -n <app_namespace> annotate ingress <ingress_iname> nginx.ingress.kubernetes.io/whitelist-source-range="+hosts_string
    os.system(cmd)
