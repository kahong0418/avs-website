import hashlib,json,os,pathlib,shutil,stat,subprocess,sys,tempfile
from urllib.request import urlopen
COMMIT='8dabccc38bedbe4dd2b239dea1060ccb827e00c7'
MANIFEST={'pcu-landing-vi.html': {'allowed_old_sha256': ['428766281916d45e59bba83b762aa39980bdeb2260e8c950d3f4c48bc6147aa1'], 'new_sha256': '9b7d82f44c769f2e8a000041c0075ef1e26fdc3384c1694e1ce67aae9dbdc41b'}, 'vi/about.html': {'allowed_old_sha256': ['128ca46587d89616aa31352ecb0ab46344529581c810c1eefd2b7ad122a2a6ed'], 'new_sha256': 'c8acaa9823b348e6597df35a107e59038935d148952eaef37b7035df1aa7f470'}, 'vi/blog-digit-size.html': {'allowed_old_sha256': ['25aef4a65f6ff85326b20c950a3809bea2ebe84f7bcb2ed5dd7da7de6a1c842d'], 'new_sha256': 'a0ffd9783d0b1cd84df6559bace0db2cfc9e11ef15deb687405f9d4459b78ff2'}, 'vi/blog-dual-colour.html': {'allowed_old_sha256': ['7e6fa1d1fe3c1f8653293781c8c791398a42564fbfd9e968d088ebb49767a589'], 'new_sha256': 'd03711495c48ef26c4747bdc2c68974c73c709eb0eb3c6154c8c03fcaf4ce3a8'}, 'vi/blog-five-digit-retrofit.html': {'allowed_old_sha256': ['9d758a00c602fa9a988125df5ad3ea66e5ebabfb5b7e998cffd2cc3dd7420092'], 'new_sha256': 'da384d46382d423814420a76a19e9741314432ea2ae1e7108d6d3f69943bbfad'}, 'vi/blog-ip-ratings.html': {'allowed_old_sha256': ['b86d713d567330bf91d4855cf2133f3f426bf542152078bb166572a0389a4a52'], 'new_sha256': 'c2c48d6df9046f7ab7c7654b5ae40538cb05f4992cfadd3d6fd929a048fea618'}, 'vi/blog-led-revolution.html': {'allowed_old_sha256': ['ef70a32f31224dc3955671d39db51025472e5f01719ecbb1c1487fec091e2e4e'], 'new_sha256': '337cd9276a8b2ecd329be853564dfc8c81fe49b5ee5869ae6f5e9e139faef4bb'}, 'vi/blog-pos-ifsf.html': {'allowed_old_sha256': ['74a4e617066497862da103c5fac423b9cec70aab0b06272aa63a0eca829c6963'], 'new_sha256': '89608fe52ec3de75c724c7e2368ddac221ec396538f7235d691ca326f176d206'}, 'vi/blog.html': {'allowed_old_sha256': ['c91f66ce8c2042309c61c7eb568cb08574af1eac166f562b3b5473e9be10100c'], 'new_sha256': '38ec0dd22842696c3a66793e543530f6594e300149c18243f1b8b806667036b9'}, 'vi/case-studies.html': {'allowed_old_sha256': ['d0afa887b148fb9cff3711bd8836dde8770686ef4a59f48837c2469cdfe23a4a'], 'new_sha256': '85880ac5f9811f9581126b3ede6cbc17aef16d4f03901e7533645490bb94082b'}, 'vi/certifications.html': {'allowed_old_sha256': ['76c7dbfd976b876d27d21736970432ba36cfefc83ba61bfc5b86be048b7fd1fd'], 'new_sha256': 'ab96ea321c3c9f79e6203553583f3e07c84e626c410cdc931b69bb2fc83b6b56'}, 'vi/contact.html': {'allowed_old_sha256': ['e73b88a77497a0b8d718243d2c71af3f0a9a27fbb3ef932f1b46187043fa0b7a'], 'new_sha256': 'bbf8c82522d0c8aca5bbccf4bb1b19f88d2db8ff5cc55cec06e4ff604db18c39'}, 'vi/distributors.html': {'allowed_old_sha256': ['e1ae993f48a68ab57a764dceedba8236f0b8733150295af6cc8c556c67e61ec5'], 'new_sha256': '10845b7f4db09062e1b01e2c0c54ee0972dacf894db9b4679f232c9317dc8670'}, 'vi/faq.html': {'allowed_old_sha256': ['84901083a0eb8197f9a3a04ab720824ec114f08b75f80c4e1b8bd95ce9271b65'], 'new_sha256': '19b88c61c53c6cc2050c1b9aa2a2726b8fb2600b0d2fcbee1a1c7613b75d42e7'}, 'vi/guides.html': {'allowed_old_sha256': ['d700dceeb6a119348b98e121ce2d692c5831686a6da7b4c0a67c86a5cc92d444'], 'new_sha256': '267fe1fb2a701fe203ea32f06671eb3a2adfa0ec4827b3316080ceecdcda713f'}, 'vi/index.html': {'allowed_old_sha256': ['705dc01b94ca7f049c5b6791dc4acfbbd82a013a07f58a113b8e40f46d04250a'], 'new_sha256': '465b56a1d14a098b7b7f5450adefca51dec6492e3d1c4e1ba5b71927327d104a'}, 'vi/integrations.html': {'allowed_old_sha256': ['b502c07335bb229c11b73456439445f1878898719fc361e8e62c31fc2a760ed4'], 'new_sha256': '9e1fc86bd1e82b13fef6a2af58aa24c41577645b2457629ae0898f246a3f7717'}, 'vi/pcu-landing.html': {'allowed_old_sha256': ['428766281916d45e59bba83b762aa39980bdeb2260e8c950d3f4c48bc6147aa1'], 'new_sha256': '9b7d82f44c769f2e8a000041c0075ef1e26fdc3384c1694e1ce67aae9dbdc41b'}, 'vi/product-athh.html': {'allowed_old_sha256': ['65513d537713bb766a4d327817a564976aebbacfcdfcdc92b2c4a028bc919ef7'], 'new_sha256': 'e8d0b550c7dc3e9cc7ce81f61ae227ad0ad90214b7ffd73491389a34f461b04e'}, 'vi/product-colorline.html': {'allowed_old_sha256': ['7c74d1e088338125f219a954741ffbfe4e44d4d83cf0e2a7aba615029d7eed91'], 'new_sha256': 'fb4506122c9a59566fe5c170b4c7a7c7dd6b8369f244af2dd8105a749e15f3fb'}, 'vi/product-controllers.html': {'allowed_old_sha256': ['9a03e87177093b552e5d340ebe05393eae67ae481d3ad2af085965360510555d'], 'new_sha256': '715a85e2ab51211530822418d4ccee33c187101864c35bc2221e8286dbbe94b2'}, 'vi/product-edge-lighting.html': {'allowed_old_sha256': ['3fe087e82902155bc83dc9433130f3b4b438812b56cfeaaaea84f58f454c2804'], 'new_sha256': 'e95f1480b1e9331b9601e0644828b1a157fc29c20b152c11edf43708e740115f'}, 'vi/product-led-modules.html': {'allowed_old_sha256': ['4a7aa1655bc36b560def1a5ea04dc26dca618d4be557b8f9dc36b1818d46ffe1'], 'new_sha256': '51b9bdf01b5ef47016bcf4c68888275fd76e5929389d348731c46b260d23a870'}, 'vi/product-led-tubes.html': {'allowed_old_sha256': ['63666c6eebdd9346ee656c16ec938782bb9e435c1a2f5ec0ce22e1a1549e24b3'], 'new_sha256': 'd2d9f6b212d546c83217d51a7bcccaf8dd46c397611972605c54813f2eefd343'}, 'vi/product-lens-strip.html': {'allowed_old_sha256': ['4a0cd8224b47fc6881aa1f4a496198069e01046260c5a25ed0bf8e769fcfbb8c'], 'new_sha256': 'fd44406910557959710a5fd1d90da8412be64428eb0b06c9ad7ebf0ce3b0e645'}, 'vi/product-pcu.html': {'allowed_old_sha256': ['e1b82216e6467f9a7698fe5513a37373162ab01a40fe4577bb746ccebbed94f7'], 'new_sha256': '7f0b153dbea3da84467da7cfd7bd31545ebcbece1b73ffb6cc1f2c3290db5fa9'}, 'vi/product-remote.html': {'allowed_old_sha256': ['d7b58554f07d724bd12364b0711805e23f6e0fe28db9baa3f591c74ebb740ccd'], 'new_sha256': 'e872ad1ea9a5a65cd288f6e03022dac759fd9ff18d3cdb9920c6cdae04cc9c15'}, 'vi/products.html': {'allowed_old_sha256': ['fc66c6defe57fcbc3ff6984546d1d127ca40e1ea5e8b07d25c65a8a7513c7916'], 'new_sha256': 'fa0ecfd8dd905ef429a38dfdd329936c4bdc4063e8344ef655b4841d24455f13'}, 'vi/quote.html': {'allowed_old_sha256': ['14447cdb3142161c61688621ec6112f14f3d278ad1b621968a208f02e59cd68b'], 'new_sha256': 'a59ae9663ec284e308166f316540c9b239732acac3a95d7f9e8a170bdaaa0ead'}, 'vi/resources.html': {'allowed_old_sha256': ['f162b7e1713721c0735b50aa836ffcc1527e86953235481a0c5f3a15be9b1a73'], 'new_sha256': '3c5546534d32661911e30625ddc13fbd11d36c2be66c4de87638f15a137fdd82'}, 'vi/solutions-petrol-stations.html': {'allowed_old_sha256': ['2f3049a9fe3cd5890341565430b7f43906a7903a9349f3639c6b3a1aa4485126'], 'new_sha256': '6892f24add05ca15be56b059d85131592bf3af5a3e57f864c1cbe515f98470dd'}, 'vi/solutions.html': {'allowed_old_sha256': ['0494185cd9ba71df20390a5d84a811dd3b15dc4618e32ee81ae5d7d05a3a51cc'], 'new_sha256': '79a4b87655f3249081e9ae3c399f5c35bd7a91bb2b8fb734cd0ae49d50305b6b'}, 'vi/support.html': {'allowed_old_sha256': ['e2c90878a1a4afcc1b2e761bc932b2bb3e5b9cb59a5d3770c8eefe4a50a82744'], 'new_sha256': '41533dbdf9ce4a8b91a1a24526fbb51518ea162cd7cf9d82243aa715ba38c70f'}}
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
        if digest not in meta['allowed_old_sha256']:raise RuntimeError('Unreviewed existing version: '+name+'. Nothing changed.')
        if sha(payload[name])!=meta['new_sha256']:raise RuntimeError('Payload checksum mismatch: '+name)
        pending.append(name)
    if not pending:print('ALREADY_INSTALLED: all 33 translation files match.');return None
    backup=pathlib.Path(tempfile.mkdtemp(prefix='.avs-vi-translation-backup-',dir=str(backup_parent)))
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
    print('UPDATED: Vietnamese translation review 2; 32 pages + legacy URL verified. English pages and WhatsApp links unchanged.')
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
