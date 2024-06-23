const Mock = require("mockjs");

Mock.mock(/friend\/friendList/, 'post', () => { //三个参数。第一个：路径，第二个：请求方式post/get，第三个：回调，返回值
    return friendList
})

Mock.mock(/friend\/chatMsg/, 'post', (config) => { //三个参数。第一个：路径，第二个：请求方式post/get，第三个：回调，返回值
    let params = JSON.parse(config.body)
    if (params.frinedId == "1002")
        return chatMsg1002
    if (params.frinedId == "1003")
        return chatMsg1003
    if (params.frinedId == "1004")
        return chatMsg1004
})

// 获取index指定的经验帖子
Mock.mock(/experience/, 'post', (config) => {
    let params = JSON.parse(config.body);
    console.log(params)
    offset = params.offset;
    job = params.job;
    company = params.company;
    ret = null;
    count = -1;
    if (job != "" && company == "") {
        console.log(`find for ${job}`)
        for (element of experienceList) {
            if (element.job == job) {
                count = count + 1;
                if (count == ofset) {
                    ret = element;
                    break;
                }
            }
        }
    }
    else if (company != "" && job == "") {
        console.log(`find for ${company}`)
        for (element of experienceList) {
            console.log(element.company)
            if (element.company == company) {
                count = count + 1;
                if (count == ofset) {
                    ret = element;
                    break;
                }
            }
        }
    }
    else if (company != "" && job != "") {
        console.log(`find for ${company} and ${job}`)
        for (element of experienceList){
            if (element.company == company && element.job == job) {
                count = count + 1;
                if (count == ofset) {
                    ret = element;
                    break;
                }
            }
        }
    }
    else if (ofset < experienceList.length) {
        ret = experienceList[ofset]
    }
    return ret;
    
})

//获取工作列表
Mock.mock(/company\/jobs/, 'post', (config) => {
    let params = JSON.parse(config.body);
    offset = params.offset;
    if (offset < jobInformationList.length){
        return jobInformationList[offset]
    }
    else{
        return null;
    }
})


let friendList = Mock.mock(
    [
        {
            img: "",
            name: "机器人1号",
            detail: "我是机器人1号",
            lastMsg: "to do",
            id: "1002",
            headImg: require("@/assets/img/head_portrait1.jpg"),
        },
        // {
        //     img: "",
        //     name: "机器人2号",
        //     detail: "我是机器人2号",
        //     lastMsg: "dada dw ertgthy j uy",
        //     id: "1003",
        //     headImg: require("@/assets/img/head_portrait2.jpg"),
        //
        // },
        // {
        //     img: "",
        //     name: "机器人3号",
        //     detail: "我是机器人3号",
        //     lastMsg: "大萨达萨达所大大萨达",
        //     id: "1004",
        //     headImg: require("@/assets/img/head_portrait3.jpg"),
        //
        // },
    ]
)

let chatMsg1002 = Mock.mock(
    [
        {
            headImg: require("@/assets/img/head_portrait.jpg"),
            name: "大毛是小白",
            time: "09：12 AM",
            msg: " 在吗？",
            chatType: 0, //信息类型，0文字，1图片
            uid: "1001", //uid
        },

        {
            headImg: require("@/assets/img/head_portrait1.jpg"),
            name: "大毛",
            time: "09：12 AM",
            msg: " 怎么了？",
            chatType: 0, //信息类型，0文字，1图片
            uid: "1002", //uid
        },
        {
            headImg: require("@/assets/img/head_portrait.jpg"),
            name: "大毛是小白",
            time: "09：12 AM",
            msg: "问你个问题",
            chatType: 0, //信息类型，0文字，1图片, 2文件
            uid: "1001",
        },
        {
            headImg: require("@/assets/img/head_portrait1.jpg"),
            name: "大毛",
            time: "09：12 AM",
            msg: "别问",
            chatType: 0, //信息类型，0文字，1图片
            uid: "1002", //uid
        },
        {
            headImg: require("@/assets/img/head_portrait.jpg"),
            name: "大毛是小白",
            time: "09：12 AM",
            msg: require("@/assets/img/emoji/slightly-smiling-face.png"),
            chatType: 1, //信息类型，0文字，1图片
            extend: {
                imgType: 1, //(1表情，2本地图片)
            },
            uid: "1001",
        },
    ]
)
let chatMsg1003 = Mock.mock(
    [
        {
            headImg: require("@/assets/img/head_portrait.jpg"),
            name: "大毛是小白",
            time: "09：12 AM",
            msg: "在干嘛呢",
            chatType: 0, //信息类型，0文字，1图片
            uid: "1001", //uid
        },
        {
            headImg: require("@/assets/img/head_portrait.jpg"),
            name: "大毛是小白",
            time: "09：12 AM",
            msg: require("@/assets/img/emoji/slightly-smiling-face.png"),
            chatType: 1, //信息类型，0文字，1图片
            extend: {
                imgType: 1, //(1表情，2本地图片)
            },
            uid: "1001",
        },
        {
            headImg: require("@/assets/img/head_portrait2.jpg"),
            name: "小毛",
            time: "09：12 AM",
            msg: "吃饭",
            chatType: 0, //信息类型，0文字，1图片
            uid: "1002", //uid
        },
        {
            headImg: require("@/assets/img/head_portrait.jpg"),
            name: "大毛是小白",
            time: "09：12 AM",
            msg: "吃的什么饭",
            chatType: 0, //信息类型，0文字，1图片, 2文件
            uid: "1001",
        },
        {
            headImg: require("@/assets/img/head_portrait2.jpg"),
            name: "小毛",
            time: "09：12 AM",
            msg: "蛋炒饭",
            chatType: 0, //信息类型，0文字，1图片
            uid: "1002", //uid
        },
        {
            headImg: require("@/assets/img/head_portrait.jpg"),
            name: "大毛是小白",
            time: "09：12 AM",
            msg: "加蛋了吗？",
            chatType: 0, //信息类型，0文字，1图片, 2文件
            uid: "1001",
        },
        {
            headImg: require("@/assets/img/head_portrait2.jpg"),
            name: "小毛",
            time: "09：12 AM",
            msg: "你说呢",
            chatType: 0, //信息类型，0文字，1图片
            uid: "1002", //uid
        },
        {
            headImg: require("@/assets/img/head_portrait2.jpg"),
            name: "小毛",
            time: "09：12 AM",
            msg: require("@/assets/img/emoji/slightly-smiling-face.png"),
            chatType: 1, //信息类型，0文字，1图片
            extend: {
                imgType: 1, //(1表情，2本地图片)
            },
            uid: "1002", //uid
        },
    ]
)
let chatMsg1004 = Mock.mock(
    [
        {
            headImg: require("@/assets/img/head_portrait.jpg"),
            name: "大毛是小白",
            time: "09：12 AM",
            msg: " sadasdawdas sadsad sad sad as despite ofhaving so much to do",
            chatType: 0, //信息类型，0文字，1图片
            uid: "1001", //uid
        },
        {
            headImg: require("@/assets/img/head_portrait.jpg"),
            name: "大毛是小白",
            time: "09：12 AM",
            msg: require("@/assets/img/emoji/slightly-smiling-face.png"),
            chatType: 1, //信息类型，0文字，1图片
            extend: {
                imgType: 1, //(1表情，2本地图片)
            },
            uid: "1001",
        },
        {
            headImg: require("@/assets/img/head_portrait3.jpg"),
            name: "小王",
            time: "09：12 AM",
            msg: " 21312大萨达萨达",
            chatType: 0, //信息类型，0文字，1图片
            uid: "1002", //uid
        },
        {
            headImg: require("@/assets/img/head_portrait.jpg"),
            name: "大毛是小白",
            time: "09：12 AM",
            msg: "111212",
            chatType: 0, //信息类型，0文字，1图片, 2文件
            uid: "1001",
        },
        {
            headImg: require("@/assets/img/head_portrait3.jpg"),
            name: "小王",
            time: "09：12 AM",
            msg: "大萨达萨达所大大萨达",
            chatType: 0, //信息类型，0文字，1图片
            uid: "1002", //uid
        },
    ]
)

let experienceList = Mock.mock(
    [
        {
            "title": "阿里云-瓴羊-后台开发 一面&二面",
            "content": "一面 60min含手撕\n'sychorinized的作用，解决什么问题\n'sychorinized作用在方法和对象上的区别\n'还有没有用过其他并发同步技术\n'CAS实现原理\n'CAS会自旋多久\n'ABA问题是什么\n'为什么会有ABA问题\n'版本号方案中版本号没有修改怎么办\n'Exception受检异常和非受检的区别\n'受检异常和非受检异常各在什么情况下使用\n'编程中如何用好两个异常\n'JVM内存泄漏是什么\n'什么情况会导致内存泄漏\n'函数重载为什么不用方法的返回值实现重载\n'怎么知道调用的重载的哪个方法\n'接口和抽象类的区别\n'还有没有其他区别\n'hashmap的底层结构\n'hashmap插入数据流程\n'hashmap解决冲突方法\n'hashmap数量特别多怎么解决插入和查找性能\n'100w数据的hashmap扩容复制会有什么问题\n'hashmap是怎么扩容的\n'hashmap的桶值是怎么计算出的\n'回到100w，hashmap扩容复制迁移数据性能影响怎么解决\n'手撕：双向链表插入+层序遍历二叉树\n'二面\n'创新创业大赛的项目是什么，几个人写的\n'大学有做过哪些不是个人写的是协作写的项目\n'微博/微信的后台推送机制是怎么实现的\n'为什么要用redis不用mysql\n'数据库有哪些索引\n'jvm的结构\n'怎么学习一门新技术\n'怎么评价你自己是一个怎么样的人\n'\n'  \n'",
            "company": "阿里",
            "job": "后端"
        },
        {
            "title": "发面经攒人品 阿里巴巴一面",
            "content": "1、讲一讲你对Spring?Boot的理解，以及为什么要用Spring?Boot？\n2、请讲一讲你了解的AOP的实现方式。\n3、除了JDK Proxy和CGLib还有别的实现AOP的方式么？\n4、请讲一讲Spring Boot简化配置具体是如何简化的。\n6、约定大于配置，Spring Boot是通过什么实现的约定大于配置？\n7、假设maven引入了两个包，可能存在版本冲突问题，那我们可以用哪些解决方案解决版本冲突问题，使两个版本的包都能在工程中被使用？\n8、如果要做一个分布式的调度系统，我们需要考虑哪些东西呢？\n9、比如我可能有一个集群来调度保证高可用，你有什么想法？\n10、JVM的内存区域和作用以及常见的GC。\n11、JVM中有哪些回收器？\n12、G1回收器的特色是什么？\n13、GC只会对堆进行GC吗？\n14、你有哪些解决线程并发问题的方案？\n17、悲观锁和乐观锁的区别。\n18、那悲观锁和乐观锁使用场景的差别是什么？\n19、那Java中想实现一个乐观锁，都有哪些方式？\n20、使用时间戳会不会有可见性问题？\n21、volatile能解决吗，就够了吗？\n22、除了加锁还有没有别的解法，绕开加锁使性能更好？\n23、讲一讲ThreadLocal使用的时候需要注意哪些点。\n24、线程并发还有别的问题吗？\n25、常用的线程池有哪些呢？\n26、那除此以外还有别的线程池吗？\n27、多线程可能涉及到信息交互，要考虑到什么？\n28、简单讲一讲线程的生命周期。\n29、有什么办法能够提升Java线程的并发能力呢？\n30、NIO了解吗？\n31、你知道有哪个框架用到NIO了吗？\n34、讲一讲String、StringBuffer和StringBuilder的区别。\n35、能讲一讲Java注解的原理和你的理解。\n36、Java注解的作用域呢？\n37、Spring Bean的scope有哪些？\n38、是否了解消息队列呢？\n39、缓存系统有哪些，了解吗？\n40、Redis为什么性能这么好的原因，你了解吗？\n41、简单说一下索引是越多越好吗？\n42、请说一下你对视图的理解。\n43、如果发现一个SQL执行的比较慢怎么办？\n44、如果Explain用到的索引不正确的话，有什么办法干预吗？\n45、算法题：String[]，找到字符串数组里的所有字符串的最长前缀。",
            "company": "阿里",
            "job": "后端"
        },
        {
            "title": "一个考研er的阿里淘天Java后端面经（补录）",
            "content": "流程还没走完，后面有进展继续更新面经～\n\n个人情况：\n一个从大三上休学半年北漂实习前端岗，到大四破釜沉舟放弃秋招准备一年408考研，到最终考完研匆匆准备春招最终决定从事后端开发方向的走了一堆弯路的苦逼。\n结果今年考研情况不容乐观，被逼无奈这个节骨眼只好战略放弃复试全心准备春招，准备一个月左右开始投递。\n? 投递进度条\n2024.2.5 BOSS上投递简历 当日通过简历 当日测评，因为临近过年暂时不安排后续流程，然后就是漫长的等待……\n2024.2.21 一面\n2024.2.22 上午笔试 下午二面\n不出意外都是通过了，等一个HR Call??\n—————————————————\n更新：\n2024.2.23 HR打电话来约了下午四点面试\n一共半个多小时 都是些结构性的问题但不知为何有点汗流浃背了 许愿OC吧 这该死的煎熬期～～#春招2024##后端开发##考研er春招找工作求助阵地##阿里巴巴淘天##大家都开始春招面试了吗#",
            "company": "阿里",
            "job": "后端"
        },
        {
            "title": "阿里云 Java 暑假实习",
            "content": "3.25  一面\n'全程90分钟，问了60分钟项目，一个八股都没问\n'算法题： 选出字符串数组中前K个频率最高的字符串\n'面试官最后说我的项目太简单了，多学一下。\n'又凉了\n'4.6  二面\n'1. 围绕着项目问问题\n'2. springboot 的循坏依赖的问题，如何解决\n'3. 如何解决mysql和redis的一致性的问题\n'4. 前端会把用户的个性化信息存放在哪？ cookie生命周期，存放在哪\n'5. session\n'6. 浏览器加载资源的流程\n'7. 对vue框架有什么看法，和评价\n'8. 在使用多线程的场景下，对框架的选择，有什么注意事项？数据一致性怎么做？\n'9. 乐观锁\n'10. 死锁问题，怎么分析死锁问题\n'11. b树和b+的树\n'12. rabbit mq的消息保障\n'13. 困难的例子，怎么解决的\n'14. 最近关注的新技术，在看什么书\n'15. 职业规划\n'16. 还在面其他的什么公司没\n'4.7 已挂",
            "company": "阿里",
            "job": "前端"
        }
    ]
)

let jobInformationList = Mock.mock(
    [
        {
            job_description: "如果你，期望参与淘天集团产品线终端（Web/Android/iOS/鸿蒙/PC等）功能的开发与实现，与视觉交互设计师一起打造最酷的用户产品；如果你，期望参与终端性能、技术架构等方面的改进与优化，打造最极致的用户体验；如果你，期望参与终端技术解决方案、工具库、框架、平台的研发，持续提升终端研发质量与效能；如果你，期望参与业内最前沿的终端技术研究和人机交互探索，拓展终端能力边界；那还犹豫什么，赶紧加入我们吧！",
            job: "终端开发工程师",
            requriement: `【必备项】
            1、本科及以上学历，计算机、软件、通信等专业优先；
            2、了解计算机原理、数据结构、设计模式、网络编程、多线程、UI 框架等基本应用开发知识；
            3、熟悉至少一门终端技术相关语言（如 JavaScript、Java/Kotlin、Swift/Objective-C、C/C++ 等）；
            4、能够面向终端界面、交互功能进行技术设计和实现，能进行局部的代码优化和改进；
            5、具备独立工作能力和解决问题的能力，善于沟通，乐于合作，善于总结分享。
            【加分项】
            1、有大型互联网公司相关岗位实习及项目开发经历；
            2、有自己的技术作品或在开源社区中有活跃贡献；
            `
        }
    ]
)

let jobList = Mock.mock(
    ["终端开发工程师", "数据产品", "算法工程师"]
)