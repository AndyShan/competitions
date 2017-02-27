# 编程之美2016
## 赛题
###初赛
平台赛，链接：[Code Hunt](https://www.codehunt.com/)
###复赛
采用团队赛的形式，基于Azure云计算平台在实际大数据的基础上展开前沿课题的较量。
在编程之美挑战赛复赛中，选手需要通过组队共同完成复赛题，考查选手编程能力的同时，也考验选手的团队协作能力。选手点此进入组队。
三人组队完成后，需要提供申请Azure账号的必要信息。然后我们会以邮件形式发送给选手Azure账号以及微软学术搜索API订阅key。
复赛题是基于微软Oxford 学术搜索API的系统编程题。Oxford 学术搜索是一个能够快速检索海量论文的搜索引擎。Oxford 学术搜索API的作用是从最新的Microsoft Academic Graph (MAG)中提取丰富的学术信息。复赛最终必须通过Azure进行提交，提交系统将在大赛官网主页公布。

Microsoft Academic Graph (MAG) is a large heterogeneous graph containing entities such as authors, papers, journals, conferences and relations between them. Microsoft provides [Academic Knowledge API](https://www.microsoft.com/cognitive-services/en-us/academic-knowledge-api) for this contest. The Entity attributes are defined [here](https://www.microsoft.com/cognitive-services/en-us/academic-knowledge-api/documentation/EntityAttributes).

Participants are supposed to provide a REST service endpoint that can find all the 1-hop, 2-hop, and 3-hop graph paths connecting a given pair of entity identifiers in MAG. The given pair of entity identifiers could be [Id, Id], [Id, AA.AuId], [AA.AuId, Id], [AA.AuId, AA.AuId]. Each node of a path should be one of the following identifiers: Id, F.Fid, J.JId, C.CId, AA.AuId, AA.AfId. Possible edges (a pair of adjacent nodes) of a path are:
![](http://studentclub.msra.cn/static/images/bop/2016/topic.png)
For each test case, the REST service endpoint will receive a JSON array via HTTP with a pair of entity identifiers, where the identifiers are 64-bit integers, e.g. [123, 456]. The service endpoint needs to respond with a JSON array within 300 seconds. The response JSON array consists of a list of graph paths in the form of [path1, path2, …, pathn], where each path is an array of entity identifiers. For example, if your program finds one 1-hop paths, two 2-hop paths, and one 3-hop paths, the results may look like this: [[123,456], [123,2,456], [123,3,456], [123,4,5,456]]. For a path such as [123,4,5,456], the integers are the identifiers of the entities on the path. After receiving the response, the evaluator will wait for a random period of time before sending the next requests.
###Evaluation Metric
The REST service must be deployed to a [Standard_A3](https://www.azure.cn/home/features/virtual-machines/#price) virtual machine for the final test. There are no constraints on the programming language you can use.

The test cases are not available before the final evaluation. When the evaluation starts, the evaluator system sends test cases to the REST endpoint of each team individually. Each team will receive 10 test cases (Q1to Q10). The response time for test case Qi is recorded as Ti(1≤i≤10). The final score is calculated using:
![这里写图片描述](http://studentclub.msra.cn/static/images/bop/2016/score.png)
where Ni is the size of the solution (<u>the total number of correct paths</u>) for Qi , Ki is <u>the total number of paths returned </u>by the REST service, Mi is the number of <u>distinct correct paths returned </u>by the REST service.
## 解题思路

 - java serlvert实现REST API
 - 灵活使用Academic Knowledge API发送请求时使用请求和并，并控制请求长度
 - 多线程并发请求

## 排名
复赛：103