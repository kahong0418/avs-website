import hashlib,json,os,pathlib,shutil,stat,subprocess,sys,tempfile
from urllib.request import urlopen
COMMIT='fe132ab8e92c9647ecc0f5578fc77e2450584e8c'
MANIFEST={'pcu-landing-vi.html': {'allowed_old_sha256': ['82877147c0b5fbc83566eedc20e0e1a54c94f0c419cdcb350bfad7739f931fd4'], 'new_sha256': '61df2a85912d95fd5397a13193eeb34aff0510959d434ec244fa6e9ff301f722'}, 'vi/about.html': {'allowed_old_sha256': ['c8acaa9823b348e6597df35a107e59038935d148952eaef37b7035df1aa7f470'], 'new_sha256': 'b155ab2eca60511f87e1ed0d8c3fd19587377183e18e0e8f54390d304a1fbda0'}, 'vi/blog-digit-size.html': {'allowed_old_sha256': ['a0ffd9783d0b1cd84df6559bace0db2cfc9e11ef15deb687405f9d4459b78ff2'], 'new_sha256': 'c98031d95ae601ea15948c55b388faa94e171f6b3332b5530c6c9373bb363219'}, 'vi/blog-dual-colour.html': {'allowed_old_sha256': ['d03711495c48ef26c4747bdc2c68974c73c709eb0eb3c6154c8c03fcaf4ce3a8'], 'new_sha256': '5d45e33cf4f6f1204089f0778f6d1a5e5922d4f61b00946514d1f833fd640907'}, 'vi/blog-five-digit-retrofit.html': {'allowed_old_sha256': ['da384d46382d423814420a76a19e9741314432ea2ae1e7108d6d3f69943bbfad'], 'new_sha256': '641123a2c6e98d1084b66526fd0f43e33e7ee057b573bc871f1d43459301b3b0'}, 'vi/blog-ip-ratings.html': {'allowed_old_sha256': ['c2c48d6df9046f7ab7c7654b5ae40538cb05f4992cfadd3d6fd929a048fea618'], 'new_sha256': '9c95783708ee6604d3150d94bd6602d8e0a401aecd34be27c8ac25675a9615b5'}, 'vi/blog-led-revolution.html': {'allowed_old_sha256': ['337cd9276a8b2ecd329be853564dfc8c81fe49b5ee5869ae6f5e9e139faef4bb'], 'new_sha256': 'df0c8a4ca07cce03f3f4de6641e7abfb1c7e31777f97bbb582d97150624d1e41'}, 'vi/blog-pos-ifsf.html': {'allowed_old_sha256': ['89608fe52ec3de75c724c7e2368ddac221ec396538f7235d691ca326f176d206'], 'new_sha256': 'bb9ee1480c14c59e448715efa1da2e0e53606db23250a50af69bd9f5b324b908'}, 'vi/blog.html': {'allowed_old_sha256': ['38ec0dd22842696c3a66793e543530f6594e300149c18243f1b8b806667036b9'], 'new_sha256': '006dfbc2bee9c7b78acde29ea47de8df6efa008c64705cb34915869cce3118ab'}, 'vi/case-studies.html': {'allowed_old_sha256': ['85880ac5f9811f9581126b3ede6cbc17aef16d4f03901e7533645490bb94082b'], 'new_sha256': '021e4956538d09fdfa296900749932e6c6c87818230348b14bd3f2734168c018'}, 'vi/certifications.html': {'allowed_old_sha256': ['ab96ea321c3c9f79e6203553583f3e07c84e626c410cdc931b69bb2fc83b6b56'], 'new_sha256': 'ae773d9fc0f23d8861fe79eec1f316fce9f800eeec764223a0a23f11f1a1f151'}, 'vi/contact.html': {'allowed_old_sha256': ['bbf8c82522d0c8aca5bbccf4bb1b19f88d2db8ff5cc55cec06e4ff604db18c39'], 'new_sha256': '010ed26ea9fb3bccac253eb1f1304b64419baa719ac8638ca5dd716037ea657c'}, 'vi/distributors.html': {'allowed_old_sha256': ['10845b7f4db09062e1b01e2c0c54ee0972dacf894db9b4679f232c9317dc8670'], 'new_sha256': '5803c52b9b4217bd8fd19b8fbc09d0dc7f8c6d2a940c083dc8be820bbe949387'}, 'vi/faq.html': {'allowed_old_sha256': ['19b88c61c53c6cc2050c1b9aa2a2726b8fb2600b0d2fcbee1a1c7613b75d42e7'], 'new_sha256': '7c8107d7c3cff004e67c902d88a65eb98b06017ecee993a33a11d3a1185e37ae'}, 'vi/guides.html': {'allowed_old_sha256': ['267fe1fb2a701fe203ea32f06671eb3a2adfa0ec4827b3316080ceecdcda713f'], 'new_sha256': '46f49a8613a685cc4bf68c0fd71293f56b0ad99ac08eecd5009ddf56063fd901'}, 'vi/index.html': {'allowed_old_sha256': ['465b56a1d14a098b7b7f5450adefca51dec6492e3d1c4e1ba5b71927327d104a'], 'new_sha256': 'c7d2d9af678ac602b2a25c7db9050b5411fe607cda537f5b0371c4955f108498'}, 'vi/integrations.html': {'allowed_old_sha256': ['9e1fc86bd1e82b13fef6a2af58aa24c41577645b2457629ae0898f246a3f7717'], 'new_sha256': '37df815e313d45de861f4b619db382c0429f3a5f0a212de1a69bb8637b230ad4'}, 'vi/pcu-landing.html': {'allowed_old_sha256': ['82877147c0b5fbc83566eedc20e0e1a54c94f0c419cdcb350bfad7739f931fd4'], 'new_sha256': '61df2a85912d95fd5397a13193eeb34aff0510959d434ec244fa6e9ff301f722'}, 'vi/product-athh.html': {'allowed_old_sha256': ['e8d0b550c7dc3e9cc7ce81f61ae227ad0ad90214b7ffd73491389a34f461b04e'], 'new_sha256': '2c69ea16a00e2a4db0965f86981dcef244d7eab57fc1a3d3a6bafbb8a86b465c'}, 'vi/product-colorline.html': {'allowed_old_sha256': ['fb4506122c9a59566fe5c170b4c7a7c7dd6b8369f244af2dd8105a749e15f3fb'], 'new_sha256': '674a800992d2fdf5ac7db263c5a321edad5c3904dccde53469a173026dfabf9e'}, 'vi/product-controllers.html': {'allowed_old_sha256': ['715a85e2ab51211530822418d4ccee33c187101864c35bc2221e8286dbbe94b2'], 'new_sha256': 'ffe835efe2c42fc8d28771ac17b6252e63e18863c6bb9fae1417e999933889b8'}, 'vi/product-edge-lighting.html': {'allowed_old_sha256': ['e95f1480b1e9331b9601e0644828b1a157fc29c20b152c11edf43708e740115f'], 'new_sha256': '8e5f7add8bec4cc887845f0a89ea6dbec764254e405f17b6d89d4a4d1d6fe648'}, 'vi/product-led-modules.html': {'allowed_old_sha256': ['51b9bdf01b5ef47016bcf4c68888275fd76e5929389d348731c46b260d23a870'], 'new_sha256': 'f0dd366ae5f1dd96b6b54b5e6919ab498070cb9a1f73c79d758486e59f8a3a6c'}, 'vi/product-led-tubes.html': {'allowed_old_sha256': ['d2d9f6b212d546c83217d51a7bcccaf8dd46c397611972605c54813f2eefd343'], 'new_sha256': '3f34f19c1275baf0100f8e30ed6e7b808b29aced818d9bd5f755217b4273a2b4'}, 'vi/product-lens-strip.html': {'allowed_old_sha256': ['fd44406910557959710a5fd1d90da8412be64428eb0b06c9ad7ebf0ce3b0e645'], 'new_sha256': '825ae7cc44fa095f14d51b3f118c0539a697deb6292f2d5d906f2781d6c18304'}, 'vi/product-pcu.html': {'allowed_old_sha256': ['7f0b153dbea3da84467da7cfd7bd31545ebcbece1b73ffb6cc1f2c3290db5fa9'], 'new_sha256': '680786e34518d51e29fdf45dba991b4840941ffcbc795b92b66fcc24928906bb'}, 'vi/product-remote.html': {'allowed_old_sha256': ['e872ad1ea9a5a65cd288f6e03022dac759fd9ff18d3cdb9920c6cdae04cc9c15'], 'new_sha256': 'a018fe7c06731af6dc2ca320e906a6bbe03850a85a965b542589297afe226cc7'}, 'vi/products.html': {'allowed_old_sha256': ['fa0ecfd8dd905ef429a38dfdd329936c4bdc4063e8344ef655b4841d24455f13'], 'new_sha256': 'd15b84b8dfca955f510db8d3038ecceeab103e23fd10834f2d4f0f1ccf04f981'}, 'vi/quote.html': {'allowed_old_sha256': ['a59ae9663ec284e308166f316540c9b239732acac3a95d7f9e8a170bdaaa0ead'], 'new_sha256': '8197ea646111ccbd152bf16a275999f3c8a16416d767c61ec2f2c80db9dc7602'}, 'vi/resources.html': {'allowed_old_sha256': ['3c5546534d32661911e30625ddc13fbd11d36c2be66c4de87638f15a137fdd82'], 'new_sha256': '2a57ceb30d2f4c41000c96686add4df32f97da04467ab8c054f9820cd0afbc8d'}, 'vi/solutions-petrol-stations.html': {'allowed_old_sha256': ['6892f24add05ca15be56b059d85131592bf3af5a3e57f864c1cbe515f98470dd'], 'new_sha256': '57297c016576f4c628f53c77b1b016d7152ff388897d4ecc141c4f0b99cfe661'}, 'vi/solutions.html': {'allowed_old_sha256': ['79a4b87655f3249081e9ae3c399f5c35bd7a91bb2b8fb734cd0ae49d50305b6b'], 'new_sha256': '3849ec9ef5f2e0f17bcb3958f72f8af84decc9361f87ebf9acb2282f79b71d2a'}, 'vi/support.html': {'allowed_old_sha256': ['41533dbdf9ce4a8b91a1a24526fbb51518ea162cd7cf9d82243aa715ba38c70f'], 'new_sha256': 'b612012e32fa3d265f0acd3391557e7ff019d20e142d65a1ba329ea279395dc7'}}
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
    if not pending:print('ALREADY_INSTALLED: Vietnamese site Zalo CTAs already match.');return None
    backup=pathlib.Path(tempfile.mkdtemp(prefix='.avs-vi-zalo-sitewide-backup-',dir=str(backup_parent)))
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
    print('UPDATED: Vietnamese site contact buttons to Zalo; '+str(len(MANIFEST))+' files verified. English pages unchanged.')
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
