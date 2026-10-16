"""Small authenticated Kubernetes client; never emits credentials."""
import base64,os,pathlib,tempfile
import requests,yaml

class Kube:
    namespace='runai-mlo-mljaggi'
    def __init__(self):
        config=yaml.safe_load(pathlib.Path('/mloscratch/homes/mljaggi/rcp-tools/kubeconfig.yaml').read_text())
        context=next(c['context'] for c in config['contexts'] if c['name']==config['current-context'])
        cluster=next(c['cluster'] for c in config['clusters'] if c['name']==context['cluster'])
        user=next(u['user'] for u in config['users'] if u['name']==context['user'])
        self.server=cluster['server']; self.session=requests.Session()
        self.session.headers['Authorization']='Bearer '+user['auth-provider']['config']['id-token']
        if 'certificate-authority-data' in cluster:
            fd,path=tempfile.mkstemp(prefix='transport-kube-ca-'); os.write(fd,base64.b64decode(cluster['certificate-authority-data'])); os.close(fd)
            self.ca=path; self.session.verify=path
        else:
            self.ca=None; self.session.verify=cluster.get('certificate-authority',True)
    def request(self,method,path,**kwargs):
        response=self.session.request(method,self.server+path,timeout=30,**kwargs)
        if not response.ok: raise RuntimeError(f'Kubernetes {method} {path}: HTTP {response.status_code}')
        return response.json()
    def close(self):
        if self.ca: pathlib.Path(self.ca).unlink(missing_ok=True)
