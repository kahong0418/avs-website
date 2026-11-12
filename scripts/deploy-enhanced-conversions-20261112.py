import hashlib,json,os,pathlib,shutil,stat,subprocess,sys,tempfile
from urllib.request import urlopen
COMMIT='a07c8c12f7bc1b9cce94ca0a33f0ddc4f5fcb6f2'
MANIFEST={'js/main.js': {'allowed_old_sha256': ['e79e6311d8dbac16e6fdb6fbf4b4fc62381d48ae6d704977514013592644afb6'], 'new_sha256': 'ac36798c66bef6621ab780a164407cb785b11f0b39c2160dbcdeaab3f0874eda'}, 'quote.html': {'allowed_old_sha256': ['77e9684c7e066134421e5aae664fb95738ceb7a7bd257ff29848a52da8c26d11'], 'new_sha256': '878bc77fd5285e47c7efe27ed833547b83bfbcc8f099aa919763a51dd6ff54ae'}, 'contact.html': {'allowed_old_sha256': ['0e8ca7f43e3b2f984d518037d15f29a85ec2a6765e24dc287cd492997c99b597'], 'new_sha256': 'f41d6db47fe47ede1bf8634e96d6ecc26c9957303095606548f1b0d693d3fb53'}}
def sha(data):return hashlib.sha256(data).hexdigest()
def safe_path(root,name):
    relative=pathlib.PurePosixPath(name)
    if relative.is_absolute() or '..' in relative.parts:raise RuntimeError('Unsafe path')
    path=root
    for part in relative.parts:
        path=path/part
        if path.is_symlink():raise RuntimeError('Symlink refused: '+name)
    return path
def current(root,name):
    p=safe_path(root,name)
    if p.exists() and not p.is_file():raise RuntimeError('Not a file: '+name)
    return p.read_bytes() if p.exists() else None

def apply_update(root,backup_parent,payload):
    before={};pending=[]
    for name,meta in MANIFEST.items():
        data=current(root,name);before[name]=data
        digest=sha(data) if data is not None else None
        if digest==meta['new_sha256']:continue
        if not (digest is None and not meta['allowed_old_sha256']) and digest not in meta['allowed_old_sha256']:raise RuntimeError('Unreviewed existing version: '+name+'. Nothing changed.')
        if sha(payload[name])!=meta['new_sha256']:raise RuntimeError('Payload checksum mismatch: '+name)
        pending.append(name)
    if not pending:print('ALREADY_INSTALLED: enhanced conversions code already live.');return None
    backup=pathlib.Path(tempfile.mkdtemp(prefix='.avs-enhanced-conv-backup-',dir=str(backup_parent)))
    for name in pending:
        if before[name] is not None:
            dest=backup/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(root/name,dest)
    (backup/'manifest.json').write_text(json.dumps(MANIFEST,indent=2))
    staged={};installed=[]
    try:
        # Stage outside web root so partial uploads cannot be served.
        for name in pending:
            dest=backup/'new'/name;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(payload[name]);staged[name]=dest
            os.chmod(dest,stat.S_IMODE((root/name).stat().st_mode) if before[name] is not None else 0o644)
        for name in MANIFEST:
            if current(root,name)!=before[name]:raise RuntimeError('Concurrent change: '+name)
        for name in pending:
            dest=safe_path(root,name);dest.parent.mkdir(parents=True,exist_ok=True)
            if current(root,name)!=before[name]:raise RuntimeError('Concurrent change: '+name)
            # cPanel account and its document root normally share one filesystem.
            os.replace(staged[name],dest);installed.append(name)
        for name,meta in MANIFEST.items():
            if sha((root/name).read_bytes())!=meta['new_sha256']:raise RuntimeError('Read-back mismatch: '+name)
    except Exception:
        for name in reversed(installed):
            dest=safe_path(root,name)
            if dest.exists() and sha(dest.read_bytes())==MANIFEST[name]['new_sha256']:
                if before[name] is None:dest.unlink()
                else:shutil.copy2(backup/name,dest)
        print('FAILED; original files restored where unchanged. Backup:',backup)
        raise
    print('UPDATED: enhanced conversions on quote/contact forms; '+str(len(MANIFEST))+' files verified.')
    print('BACKUP:',backup);print('COMMIT:',COMMIT);return backup

def main():
    uapi=shutil.which('uapi') or '/usr/local/cpanel/bin/uapi'
    result=json.loads(subprocess.check_output([uapi,'--output=json','DomainInfo','single_domain_data','domain=avs.my'],timeout=30))['result']
    info=result.get('data') or {}
    if result.get('status')!=1 or info.get('domain')!='avs.my' or not os.path.isabs(info.get('documentroot','')):raise RuntimeError('Cannot verify avs.my document root')
    root=pathlib.Path(info['documentroot']).resolve(strict=True);backup_parent=pathlib.Path.home().resolve()
    if backup_parent==root or root in backup_parent.parents:raise RuntimeError('Backup must be outside document root')
    payload={}
    for name,meta in MANIFEST.items():
        with urlopen('https://raw.githubusercontent.com/kahong0418/avs-website/'+COMMIT+'/'+name,timeout=30) as response:payload[name]=response.read(2000000)
        if sha(payload[name])!=meta['new_sha256']:raise RuntimeError('Download checksum mismatch: '+name)
    apply_update(root,backup_parent,payload)
if __name__=='__main__':
    try:main()
    except Exception as e:sys.exit('STOP: '+str(e))
