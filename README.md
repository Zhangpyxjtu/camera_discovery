# camera_discovery
摄像头自动发现
### onvif 扫描协议

### 传入参数

自带参数
export edgenodeKey="dell31312312313"

填写的参数
export user="admin"
export pwd="a123456789"
export url="http://101.206.211.222:8003/mec/v1/device/edge-endpoint/"
#camera-discovery sensecam-discovery

### 数据库参数
application_name: onvif扫描协议
scene: 该协议可以将本地的具有onvif协议的摄像头自动扫描， 并且发送到云端

template_name: onvif扫描
template_desc: 扫描本地摄像头并且发送到云端

```json
{
    "commonVariable": [
        {
            "title": "onvif 用户名",
            "key": "user",
            "value": ""
        },
        {
            "title": "onvif 密码",
            "key": "pwd",
            "value": ""
        },
        {
            "title": "推送的地址",
            "key": "url",
            "value": ""
        },
        {
            "title": "harbor地址",
            "key": "PLATFORM_HARBOR_URL",
            "value": ""
        }
    ],
    "environmentVariable": [],
    "showVariable": []
}
{
    "commonVariable": [
        {
            "title": "推送的地址",
            "key": "url",
            "value": ""
        },
        {
            "title": "harbor地址",
            "key": "PLATFORM_HARBOR_URL",
            "value": ""
        }
    ],
    "environmentVariable": [],
    "showVariable": []
}
```

helm --kubeconfig ~/.kube/config-unicom install --set-string PLATFORM_HARBOR_URL=101.206.211.217:8079/mec/,user="admin",pwd="a123456789",url="http://101.206.211.217:8003/mec/v1/device/edge-endpoint/",hostname=dell31312312313  onvif-test ../charts/onvif-discovery-amd64


mysql -h 192.168.31.121 --port 3307 -u root -p < db.sql
test

# ability

全部能力以及部署界面

# ELK


# 边缘市场手动创建能力
application:
字段描述:
application_type: 类型:1.能力;2.应用
application_permission: 权限:1.通用;2.私有;
tenant_id: 当权限为通用时租户主键为0
type: "人工智能":1,  "物联网":2 , "数据采集":3  , "区块链":4
arch: AMD64: 1 , ARM64: 2 , ARM32: 3
industry: 智慧校园: 1, 智慧社区: 2, 智慧园区: 3

deploy_template: 
sort: 模板展示的顺序
cpu, memory: 该能力需要的CPU以及内存
variable_template: 配置commonVariable展示参数， 在能力部署时可见 
{
    "commonVariable":[
        {
            "title":"mysql 端口",
            "key":"ENV_MYSQL_PORT",
            "value":""
        }
    ],
    "environmentVariable":[
    ],
    "showVariable":[
    ]
}
