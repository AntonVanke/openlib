## /OpenLib v0.0.1
```text
暂无描述
```
#### 公共Header参数
参数名 | 示例值 | 参数描述
--- | --- | ---
暂无参数
#### 公共Query参数
参数名 | 示例值 | 参数描述
--- | --- | ---
暂无参数
#### 公共Body参数
参数名 | 示例值 | 参数描述
--- | --- | ---
暂无参数
#### 预执行脚本
```javascript
apt.variables.set("host", "http://127.0.0.1:5000");
```
#### 后执行脚本
```javascript
暂无后执行脚本
```
## /OpenLib/登录
```text
暂无描述
```
#### 接口状态
> 开发中

#### 接口URL
> {{host}}/login

#### 请求方式
> POST

#### Content-Type
> application/json

#### 请求Body参数
```javascript
{"username": "10001","password": "123456"}
// {"username": "311809030326","password": "11111111a"}
```
#### 预执行脚本
```javascript
暂无预执行脚本
```
#### 后执行脚本
```javascript
apt.globals.set("key",response.json.data.token);
apt.globals.get("key");

```
#### 成功响应示例
```javascript
{
	"code": 200,
	"data": {
		"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY1MjUxOTk5OSwianRpIjoiNjRiOGQyNmMtNGFjYy00Yjg1LWI5ZTgtNzhhYTRkMTVmNzBlIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNjUyNTE5OTk5LCJleHAiOjE2NTI1MjcxOTl9.6A66PF_jHImi4FeqyIpeSKtjWdVUtaCPELY-slFEf-w"
	},
	"message": "success"
}
```
参数名 | 示例值 | 参数类型 | 参数描述
--- | --- | --- | ---
code | 200 | Number | 状态码
data | - | Object | 返回数据
data.token | eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY1MjUxOTk5OSwianRpIjoiNjRiOGQyNmMtNGFjYy00Yjg1LWI5ZTgtNzhhYTRkMTVmNzBlIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNjUyNTE5OTk5LCJleHAiOjE2NTI1MjcxOTl9.6A66PF_jHImi4FeqyIpeSKtjWdVUtaCPELY-slFEf-w | String | 认证令牌
message | success | String | 状态信息
#### 错误响应示例
```javascript
{
	"code": 202,
	"data": null,
	"message": "Wrong password"
}
```
参数名 | 示例值 | 参数类型 | 参数描述
--- | --- | --- | ---
code | 202 | Number | 状态码
data | - | Object | 返回数据
message | Wrong password | String | 状态信息
## /OpenLib/获取用户信息
```text
暂无描述
```
#### 接口状态
> 开发中

#### 接口URL
> {{host}}/user

#### 请求方式
> GET

#### Content-Type
> multipart/form-data

#### 请求Body参数
```javascript

```
#### 预执行脚本
```javascript
暂无预执行脚本
```
#### 后执行脚本
```javascript
暂无后执行脚本
```
#### 成功响应示例
```javascript
{
	"code": 200,
	"message": "success",
	"data": {
		"id": 1,
		"username": "311809030326",
		"name": "冯君奭",
		"school": "河南理工大学",
		"college": "计算机学院",
		"major": "信息管理与信息系统",
		"class_name": "1803",
		"enabled": 1
	}
}
```
参数名 | 示例值 | 参数类型 | 参数描述
--- | --- | --- | ---
code | 200 | Number | 状态码
message | success | String | 状态信息
data | - | Object | 返回数据
data.id | 1 | Number | 用户ID
data.username | 311809030326 | String | 用户名
data.name | 冯君奭 | String | 真实名称
data.school | 河南理工大学 | String | 学校
data.college | 计算机学院 | String | 学院
data.major | 信息管理与信息系统 | String | 专业
data.class_name | 1803 | String | 班级
data.enabled | 1 | Number | 是否启用
## /OpenLib/修改密码
```text
暂无描述
```
#### 接口状态
> 开发中

#### 接口URL
> {{host}}/user

#### 请求方式
> POST

#### Content-Type
> application/json

#### 请求Body参数
```javascript
{
    "old_password": "123456",
    "new_password": "11111111a"
}
```
#### 预执行脚本
```javascript
暂无预执行脚本
```
#### 后执行脚本
```javascript
暂无后执行脚本
```
#### 错误响应示例
```javascript
{
	"code": 201,
	"message": "Invalid Password",
	"data": null
}
```
## /OpenLib/预约座位
```text
暂无描述
```
#### 接口状态
> 开发中

#### 接口URL
> {{host}}/reserve

#### 请求方式
> POST

#### Content-Type
> application/json

#### 请求Body参数
```javascript
{
    "seat_id": 1,
    "start_time": 1652709600,
    "end_time": 1652709600
}
```
#### 预执行脚本
```javascript
暂无预执行脚本
```
#### 后执行脚本
```javascript
暂无后执行脚本
```
#### 成功响应示例
```javascript
{
	"code": 200,
	"message": "success",
	"data": [
		{
			"start_time": 1652673600,
			"id": 1,
			"cancelled": 0,
			"user_id": 1,
			"seat_id": 1,
			"end_time": 1652677200,
			"create_time": "2022-05-16 18:11:53"
		},
		{
			"start_time": 1652702400,
			"id": 9,
			"cancelled": 0,
			"user_id": 1,
			"seat_id": 1,
			"end_time": 1652706000,
			"create_time": "2022-05-16 18:38:05"
		}
	]
}
```
参数名 | 示例值 | 参数类型 | 参数描述
--- | --- | --- | ---
code | 200 | Number | 状态码
message | success | String | 状态信息
data | - | Object | 返回数据
data.start_time | 1652673600 | Number | 预约开始时间
data.id | 1 | Number | 用户ID
data.cancelled | - | Number | 是否取消
data.user_id | 1 | Number | 预约用户
data.seat_id | 1 | Number | 预约座位ID
data.end_time | 1652677200 | Number | 预约结束时间
data.create_time | 2022-05-16 18:11:53 | String | 预约创建时间
#### 错误响应示例
```javascript
{
	"code": 202,
	"message": "Invalid appointment time",
	"data": {
		"available_time_period": [
			[
				1652652000,
				1652673600
			],
			[
				1652677200,
				1652702400
			],
			[
				1652706000,
				1652709600
			]
		]
	}
}
```
参数名 | 示例值 | 参数类型 | 参数描述
--- | --- | --- | ---
code | 202 | Number | 状态码
message | Invalid appointment time | String | 状态信息
data | - | Object | 返回数据
data.available_time_period | - | Object | 可用时间段
data.available_time_period.0 | 1652652000 | Number | 开始时间
data.available_time_period.1 | 1652673600 | Number | 结束时间
## /OpenLib/获取设置
```text
暂无描述
```
#### 接口状态
> 开发中

#### 接口URL
> {{host}}/option

#### 请求方式
> GET

#### Content-Type
> multipart/form-data

#### 请求Body参数
```javascript

```
#### 预执行脚本
```javascript
暂无预执行脚本
```
#### 后执行脚本
```javascript
暂无后执行脚本
```
#### 成功响应示例
```javascript
{
	"code": 200,
	"message": "success",
	"data": [
		{
			"name": "web_name",
			"value": "河南理工大学图书馆座位预约系统",
			"id": 1
		},
		{
			"name": "web_url",
			"value": "http://127.0.0.1/",
			"id": 2
		},
		{
			"name": "max_hour",
			"value": "4",
			"id": 3
		},
		{
			"name": "open_time",
			"value": "6:00",
			"id": 4
		},
		{
			"name": "close_time",
			"value": "22:00",
			"id": 5
		}
	]
}
```
参数名 | 示例值 | 参数类型 | 参数描述
--- | --- | --- | ---
code | 200 | Number | 状态码
message | success | String | 状态信息
data | - | Object | 返回数据
data.name | web_name | String | 真实名称
data.value | 河南理工大学图书馆座位预约系统 | String | 
data.id | 1 | Number | 用户ID
## /OpenLib/获取预约
```text
暂无描述
```
#### 接口状态
> 开发中

#### 接口URL
> {{host}}/reserve/2

#### 请求方式
> GET

#### Content-Type
> multipart/form-data

#### 请求Body参数
```javascript

```
#### 预执行脚本
```javascript
暂无预执行脚本
```
#### 后执行脚本
```javascript
暂无后执行脚本
```
#### 成功响应示例
```javascript
{
	"code": 200,
	"message": "success",
	"data": [
		{
			"start_time": 1652673600,
			"id": 1,
			"cancelled": 0,
			"user_id": 1,
			"seat_id": 1,
			"end_time": 1652677200,
			"create_time": "2022-05-16 18:11:53"
		},
		{
			"start_time": 1652702400,
			"id": 7,
			"cancelled": 1,
			"user_id": 1,
			"seat_id": 1,
			"end_time": 1652706000,
			"create_time": "2022-05-16 18:11:53"
		},
		{
			"start_time": 1652702400,
			"id": 8,
			"cancelled": 0,
			"user_id": 1,
			"seat_id": 1,
			"end_time": 1652706000,
			"create_time": "2022-05-16 18:23:38"
		}
	]
}
```
参数名 | 示例值 | 参数类型 | 参数描述
--- | --- | --- | ---
code | 200 | Number | 状态码
message | success | String | 状态信息
data | - | Object | 返回数据
data.start_time | 1652673600 | Number | 预约开始时间
data.id | 1 | Number | 用户ID
data.cancelled | - | Number | 是否取消
data.user_id | 1 | Number | 预约用户
data.seat_id | 1 | Number | 预约座位ID
data.end_time | 1652677200 | Number | 预约结束时间
data.create_time | 2022-05-16 18:11:53 | String | 预约创建时间
## /OpenLib/获取场馆
```text
暂无描述
```
#### 接口状态
> 开发中

#### 接口URL
> {{host}}/building

#### 请求方式
> GET

#### Content-Type
> form-data

#### 预执行脚本
```javascript
暂无预执行脚本
```
#### 后执行脚本
```javascript
暂无后执行脚本
```
#### 成功响应示例
```javascript
{
	"code": 200,
	"message": "success",
	"data": [
		{
			"id": 1,
			"name": "第三图书馆",
			"enabled": 1
		},
		{
			"id": 5,
			"name": "北校区图书馆",
			"enabled": 1
		},
		{
			"id": 9,
			"name": "南校区图书馆",
			"enabled": 1
		}
	]
}
```
## /OpenLib/获取场馆内的房间
```text
暂无描述
```
#### 接口状态
> 开发中

#### 接口URL
> {{host}}/building/:building_id

#### 请求方式
> GET

#### Content-Type
> form-data

#### 路径变量
参数名 | 示例值 | 参数描述
--- | --- | ---
building_id | 1 | 场馆ID
#### 预执行脚本
```javascript
暂无预执行脚本
```
#### 后执行脚本
```javascript
暂无后执行脚本
```
#### 成功响应示例
```javascript
{
	"code": 200,
	"message": "success",
	"data": [
		{
			"name": "第一阅览厅",
			"enabled": 1,
			"id": 1,
			"building_id": 1
		}
	]
}
```
## /OpenLib/获取房间
```text
暂无描述
```
#### 接口状态
> 开发中

#### 接口URL
> {{host}}/room

#### 请求方式
> GET

#### Content-Type
> form-data

#### 预执行脚本
```javascript
暂无预执行脚本
```
#### 后执行脚本
```javascript
暂无后执行脚本
```
#### 成功响应示例
```javascript
{
	"code": 200,
	"message": "success",
	"data": [
		{
			"building_id": 1,
			"enabled": 1,
			"id": 1,
			"name": "第一阅览厅"
		}
	]
}
```
参数名 | 示例值 | 参数类型 | 参数描述
--- | --- | --- | ---
code | 200 | Number | 状态码
message | success | String | 状态信息
data | - | Object | 返回数据
data.building_id | 1 | Number | 建筑ID
data.enabled | 1 | Number | 是否启用
data.id | 1 | Number | 房间ID
data.name | 第一阅览厅 | String | 房间名称
## /OpenLib/获取房间内的座位
```text
暂无描述
```
#### 接口状态
> 开发中

#### 接口URL
> {{host}}/room/:room_id

#### 请求方式
> GET

#### Content-Type
> form-data

#### 路径变量
参数名 | 示例值 | 参数描述
--- | --- | ---
room_id | 1 | 房间ID
#### 预执行脚本
```javascript
暂无预执行脚本
```
#### 后执行脚本
```javascript
暂无后执行脚本
```
#### 成功响应示例
```javascript
{
	"code": 200,
	"message": "success",
	"data": [
		{
			"id": 1,
			"room_id": 1,
			"enabled": 0
		}
	]
}
```
参数名 | 示例值 | 参数类型 | 参数描述
--- | --- | --- | ---
code | 200 | Number | 状态码
message | success | String | 状态信息
data | - | Object | 返回数据
data.id | 1 | Number | 座位ID
data.room_id | 1 | Number | 房间ID
data.enabled | - | Number | 是否启用
## /OpenLib/获取座位有效预约时段
```text
暂无描述
```
#### 接口状态
> 开发中

#### 接口URL
> {{host}}/seat/:seat_id

#### 请求方式
> GET

#### Content-Type
> form-data

#### 路径变量
参数名 | 示例值 | 参数描述
--- | --- | ---
seat_id | 1 | 座位ID
#### 预执行脚本
```javascript
暂无预执行脚本
```
#### 后执行脚本
```javascript
暂无后执行脚本
```
## /OpenLib/新增场馆
```text
暂无描述
```
#### 接口状态
> 开发中

#### 接口URL
> {{host}}/building

#### 请求方式
> POST

#### Content-Type
> json

#### 请求Body参数
```javascript
{
	"name": "南校区第一图书馆",
	"enabled": 1
}
```
参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述
--- | --- | --- | --- | ---
name | 河南理工大学北校区图书馆 | String | 是 | 真实名称
enabled | 1 | Number | 是 | 是否启用
#### 预执行脚本
```javascript
暂无预执行脚本
```
#### 后执行脚本
```javascript
暂无后执行脚本
```
#### 成功响应示例
```javascript
{
	"code": 200,
	"message": "success",
	"data": null
}
```
#### 错误响应示例
```javascript
{
	"code": 203,
	"message": "Duplicate fields: [name]:`北校区图书馆`",
	"data": null
}
```
## /OpenLib/删除场馆
```text
暂无描述
```
#### 接口状态
> 开发中

#### 接口URL
> {{host}}/building/:building_id

#### 请求方式
> POST

#### Content-Type
> json

#### 路径变量
参数名 | 示例值 | 参数描述
--- | --- | ---
building_id | 9 | -
#### 请求Body参数
```javascript
{
    "_method": "delete"
}
```
#### 预执行脚本
```javascript
暂无预执行脚本
```
#### 后执行脚本
```javascript
暂无后执行脚本
```
#### 成功响应示例
```javascript
{
	"code": 200,
	"message": "success",
	"data": null
}
```
#### 错误响应示例
```javascript
{
	"code": 209,
	"message": "[id]:5: Not Found",
	"data": null
}
```
## /OpenLib/编辑场馆
```text
暂无描述
```
#### 接口状态
> 开发中

#### 接口URL
> {{host}}/building/:building_id

#### 请求方式
> PUT

#### Content-Type
> json

#### 路径变量
参数名 | 示例值 | 参数描述
--- | --- | ---
building_id | 1 | 场馆ID
#### 请求Body参数
```javascript
{
	"name": "南校区第二图书馆",
    "enabled": 1
}
```
#### 预执行脚本
```javascript
暂无预执行脚本
```
#### 后执行脚本
```javascript
暂无后执行脚本
```
#### 成功响应示例
```javascript
{
	"code": 200,
	"message": "success",
	"data": null
}
```
## /OpenLib/修改设置
```text
暂无描述
```
#### 接口状态
> 开发中

#### 接口URL
> {{host}}/option/:name

#### 请求方式
> POST

#### Content-Type
> json

#### 路径变量
参数名 | 示例值 | 参数描述
--- | --- | ---
name | test | -
#### 请求Body参数
```javascript
{
    "value": "test"
}
```
#### 预执行脚本
```javascript
暂无预执行脚本
```
#### 后执行脚本
```javascript
暂无后执行脚本
```
## /OpenLib/取消预约
```text
暂无描述
```
#### 接口状态
> 开发中

#### 接口URL
> {{host}}/reserve/1

#### 请求方式
> DELETE

#### Content-Type
> application/json

#### 请求Body参数
```javascript
{
    "_method": "delete"
}
```
#### 预执行脚本
```javascript
暂无预执行脚本
```
#### 后执行脚本
```javascript
暂无后执行脚本
```
#### 成功响应示例
```javascript
{
	"code": 200,
	"message": "success",
	"data": null
}
```
#### 错误响应示例
```javascript
{
	"code": 205,
	"message": "Invalid reservation",
	"data": null
}
```