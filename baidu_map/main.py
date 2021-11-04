
import time
from urllib.parse import quote

import requests
gsm = '1e'
for page in range(20):
    title = "一字肩领"
    page = page*30
    url = f"https://image.baidu.com/search/acjson?tn=resultjson_com&logid=7987472356744145319&ipn=rj&ct=201326592&is=&fp=result&queryWord={quote(title)}&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&hd=&latest=&copyright=&word={quote(title)}&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&expermode=&nojc=&pn={page}&rn=30&gsm={gsm}"
    payload = {}
    headers = {
    'Connection': 'keep-alive',
    'Accept': 'text/plain, */*; q=0.01',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=index&fr=&hs=0&xthttps=111110&sf=1&fmq=&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&word=%E5%9C%86%E9%A2%86&oq=%E5%9C%86%E9%A2%86&rsp=-1',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cookie': 'BDqhfp=%E5%9C%86%E9%A2%86%26%260-10-1undefined%26%265403%26%264; BIDUPSID=D180B68369D62E352A13BE6FA63675E6; PSTM=1634714110; BAIDUID=D180B68369D62E356E4E472DD3B7909B:FG=1; __yjs_duid=1_6ed0befb0a7b56ec5570e4663a3d6d151634724680598; BDUSS=zB3SUNpWjh5Q2xPZnVJQ1dJdmJZUE9rcUlCbFdJTVdDWHQydDN4ZlJ2Qkc4cUZoSVFBQUFBJCQAAAAAAAAAAAEAAAAG53QxsOvSucz0tca~tMutAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEZlemFGZXphY; BDUSS_BFESS=zB3SUNpWjh5Q2xPZnVJQ1dJdmJZUE9rcUlCbFdJTVdDWHQydDN4ZlJ2Qkc4cUZoSVFBQUFBJCQAAAAAAAAAAAEAAAAG53QxsOvSucz0tca~tMutAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEZlemFGZXphY; H_PS_PSSID=; BAIDUID_BFESS=D180B68369D62E356E4E472DD3B7909B:FG=1; delPer=0; PSINO=5; BDORZ=FFFB88E999055A3F8A630C64834BD6D0; BCLID=8220388553491528475; BDSFRCVID=5vIOJexroG01_AOHqnUaJTSnheKKTS5TDYrEK53BcOL85g_Vg2RdEG0Pt_ebCZI-dB_fogKK0eOTHk-F_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF=fRk8VIDyJCvbfP0kb4QKb4L3-UAX5-Cs2KJi2hcHMPoosItlQMQ-y-Kz2bnZLpJX2ITiaMbRJxbUotoHyT_5L4tgXaAtKhRp5brN0p5TtUJM_n5PLp6zqt0YBUjyKMnitIT9-pnoHlQrh459XP68bTkA5bjZKxtq3mkjbPbDfn028DKuejtBe5objHRabK6aKC5bL6rJabC38D5MXU6q2bDeQN0D0UoqWIclW4jFQUO_jb5oypO6jq0vWq54WbbvLT7johRTWqR4eIo-bMonDh83BUoa3hTAHCnGMbQO5hvvhb5O3M7OqfKmDloOW-TB5bbPLUQF5l8-sq0x0bOte-bQXH_EJj8qJn-j_K_Q-J5fjtoN-n8_KPFD-xLX-PoyKD6ysJOOaCvkslvOy4oTj6DFQhrrh6575ecXaqcmLbrsOhoMet7j3MvB-fnht-JpJ2Q43K5Y3lcAHx0wQft20-IIeMtjBbQaWDjhQn7jWhk2eq72y-RMQlRX5q79atTMfNTJ-qcH0KQpsIJM5-DWbT8IjHCeJjt8JJCjoKv5b-0_HRcTMb6OMRvH-UnLq-uj3eOZ0l8KtJT1hb7CMx7tQ4C1yROg2tv-WbTyoDOmWIQHDU8xyfcdyJ_W5RrBBqRuQNv4KKJxBRLWeIJo5t5T3f4fhUJiB5O-Ban7B-bIXKohJh7FM4tW3J0ZyxomtfQxtNRJ0DnjtnLhbCI6ejAae5QM5pJfet5K-Dc-LnOSHJO_bI5CyfnkbJkXhPtjJlRCB2bDWf5qWfb6DRnNyURx0TL7QbrH0xPtt2r22h4yJR3rSR0404OpQT8r5bn-5fJzW4jb5f7Dab3vOIJNXpO1MIuzBN5thURB2DkO-4bCWJ5TMl5jDh3Mb6ksD-FtqtJHKbDtoKPMtUK; BCLID_BFESS=8220388553491528475; BDSFRCVID_BFESS=5vIOJexroG01_AOHqnUaJTSnheKKTS5TDYrEK53BcOL85g_Vg2RdEG0Pt_ebCZI-dB_fogKK0eOTHk-F_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF_BFESS=fRk8VIDyJCvbfP0kb4QKb4L3-UAX5-Cs2KJi2hcHMPoosItlQMQ-y-Kz2bnZLpJX2ITiaMbRJxbUotoHyT_5L4tgXaAtKhRp5brN0p5TtUJM_n5PLp6zqt0YBUjyKMnitIT9-pnoHlQrh459XP68bTkA5bjZKxtq3mkjbPbDfn028DKuejtBe5objHRabK6aKC5bL6rJabC38D5MXU6q2bDeQN0D0UoqWIclW4jFQUO_jb5oypO6jq0vWq54WbbvLT7johRTWqR4eIo-bMonDh83BUoa3hTAHCnGMbQO5hvvhb5O3M7OqfKmDloOW-TB5bbPLUQF5l8-sq0x0bOte-bQXH_EJj8qJn-j_K_Q-J5fjtoN-n8_KPFD-xLX-PoyKD6ysJOOaCvkslvOy4oTj6DFQhrrh6575ecXaqcmLbrsOhoMet7j3MvB-fnht-JpJ2Q43K5Y3lcAHx0wQft20-IIeMtjBbQaWDjhQn7jWhk2eq72y-RMQlRX5q79atTMfNTJ-qcH0KQpsIJM5-DWbT8IjHCeJjt8JJCjoKv5b-0_HRcTMb6OMRvH-UnLq-uj3eOZ0l8KtJT1hb7CMx7tQ4C1yROg2tv-WbTyoDOmWIQHDU8xyfcdyJ_W5RrBBqRuQNv4KKJxBRLWeIJo5t5T3f4fhUJiB5O-Ban7B-bIXKohJh7FM4tW3J0ZyxomtfQxtNRJ0DnjtnLhbCI6ejAae5QM5pJfet5K-Dc-LnOSHJO_bI5CyfnkbJkXhPtjJlRCB2bDWf5qWfb6DRnNyURx0TL7QbrH0xPtt2r22h4yJR3rSR0404OpQT8r5bn-5fJzW4jb5f7Dab3vOIJNXpO1MIuzBN5thURB2DkO-4bCWJ5TMl5jDh3Mb6ksD-FtqtJHKbDtoKPMtUK; BDRCVFR[3iF-CRdS3ws]=mk3SLVN4HKm; BA_HECTOR=0g002h208g2121a4ar1gnvc770q; BDRCVFR[X_XKQks0S63]=mk3SLVN4HKm; userFrom=www.baidu.com; firstShowTip=1; indexPageSugList=%5B%22%E5%9C%86%E9%A2%86%22%5D; cleanHistoryStatus=0; BDRCVFR[dG2JNJb_ajR]=mk3SLVN4HKm; ab_sr=1.0.1_ZjUxODk4YzU0ZDY3NTM1ZTViODYwZDM5MjVmZTM0MTQxOTc2NDRkMzQ2MzY1MmVjMTZiMTFhNWRiM2U4ZjQ2ZDNiMTg2NmQ2ZjFkMjMzNzI0MTEwZmJkMDI5NjRhMzRiY2E2NTE0Y2Q0YjI0ODFiMWZmZDY5ZGZmNWUzMjkxNzA0MmNmMThiYzc4NzUxOGJmMmE0MWU0NGFhNTY5YmNlN2IxZGI0NmMzMWU1MzRkMDRkNTE4YWFiMjcxMThhYmMw; BDRCVFR[-pGxjrCMryR]=mk3SLVN4HKm; BDRCVFR[-pGxjrCMryR]=mk3SLVN4HKm'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()['data']
    gsm = response.json()['gsm']

    for info in data:
        if info == {}:
            continue
        thumbURL = info['thumbURL']
        print(thumbURL)
        image_name = str(int(time.time()*1000))
        resp = requests.get(thumbURL)
        open(rf'/home/ledi/桌面/data/jin-yi-wei/baidu_map/image/{title}/{image_name}.jpg', 'wb').write(resp.content)


