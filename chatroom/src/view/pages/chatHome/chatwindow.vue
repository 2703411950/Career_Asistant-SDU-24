<template>
  <div class="chat-window">
    <div class="top">
      <div class="head-pic">
        <HeadPortrait :imgUrl="frinedInfo.headImg"></HeadPortrait>
      </div>
      <div class="info-detail">
        <div class="name">{{ "模拟面试助手" }}</div>
        <div class="detail">{{ "你的专业求职帮手" }}</div>
      </div>
      <div class="other-fun">
        <span class="iconfont icon-shipin" @click="video"> </span>
        <span class="iconfont icon-gf-telephone" @click="telephone"></span>
        <label for="docFile">
          <span class="iconfont icon-wenjian"></span>
        </label>
        <label for="imgFile">
          <span class="iconfont icon-tupian"></span>
        </label>
        <input
            type="file"
            name=""
            id="imgFile"
            @change="sendImg"
            accept="image/*"
        />
        <input
            type="file"
            name=""
            id="docFile"
            @change="sendFile"
            accept="application/*,text/*"
        />
        <!-- accept="application/*" -->
      </div>
    </div>
    <div class="botoom">
      <div class="chat-content" ref="chatContent">
        <div class="chat-wrapper" v-for="item in chatList" :key="item.id">
          <div class="chat-friend" v-if="item.uid !== '1001'">
            <div class="chat-text" v-if="item.chatType == 0">
              {{ item.msg }}
            </div>
            <div class="chat-img" v-if="item.chatType == 1">
              <img
                  :src="item.msg"
                  alt="表情"
                  v-if="item.extend.imgType == 1"
                  style="width: 100px; height: 100px"
              />
              <el-image :src="item.msg" :preview-src-list="srcImgList" v-else>
              </el-image>
            </div>
            <div class="chat-img" v-if="item.chatType == 2">
              <div class="word-file">
                <FileCard
                    :fileType="item.extend.fileType"
                    :file="item.msg"
                ></FileCard>
              </div>
            </div>
            <div class="info-time">
              <img :src="item.headImg" alt=""/>
              <span>{{ item.name }}</span>
              <span>{{ item.time }}</span>
            </div>
          </div>
          <div class="chat-me" v-else>
            <div class="chat-text" v-if="item.chatType == 0">
              {{ item.msg }}
            </div>
            <div class="chat-img" v-if="item.chatType == 1">
              <img
                  :src="item.msg"
                  alt="表情"
                  v-if="item.extend.imgType == 1"
                  style="width: 100px; height: 100px"
              />
              <el-image
                  style="max-width: 300px; border-radius: 10px"
                  :src="item.msg"
                  :preview-src-list="srcImgList"
                  v-else
              >
              </el-image>
            </div>
            <div class="chat-img" v-if="item.chatType == 2">
              <div class="word-file">
                <FileCard
                    :fileType="item.extend.fileType"
                    :file="item.msg"
                ></FileCard>
              </div>
            </div>
            <div class="chat-audio" v-if="item.chatType == 3 && item.audioBlob">
              <audio controls :src="getObjectURL(item.audioBlob)"></audio>
            </div>
            <div class="info-time">
              <span>{{ item.name }}</span>
              <span>{{ item.time }}</span>
              <img :src="item.headImg" alt=""/>
            </div>
          </div>
        </div>
      </div>
      <div class="chatInputs">
        <!--        <div class="emoji boxinput" @click="clickEmoji">-->
        <!--          <img src="@/assets/img/emoji/smiling-face.png" alt=""/>-->
        <!--        </div>-->

        <!--        语音-->
        <!--        <div class="emoji-content">-->
        <div v-if="isRecording" style="display: flex">
          <div class="send boxinput" style="margin-right: 10px" @click="stopRecording">
            <img src="@/assets/img/emoji/no.png" alt=""/>
          </div>
          <span style="display: flex; justify-content: center; align-items: center;">{{ recordedTime }}s</span>
          <div class="send boxinput" style="margin-left: 10px" @click="saveRecording">
            <img src="@/assets/img/emoji/yes.png" alt=""/>
          </div>
        </div>
        <div v-else class="send boxinput" @click="startRecording">
          <img src="@/assets/img/emoji/audio1.png" alt=""/>
        </div>
        <input class="inputs" v-model="inputMsg" @keyup.enter="sendText"/>
        <div class="send boxinput" @click="sendText">
          <img src="@/assets/img/emoji/rocket.png" alt=""/>
        </div>
        <!--          <Emoji-->
        <!--              v-show="showEmoji"-->
        <!--              @sendEmoji="sendEmoji"-->
        <!--              @closeEmoji="clickEmoji"-->
        <!--          ></Emoji>-->
        <!--        </div>-->

      </div>

    </div>
  </div>
</template>

<script>
import {animation} from "@/util/util";
import {getChatMsg} from "@/api/getData";

//必须引入的核心
import Recorder from 'recorder-core';

//引入mp3格式支持文件；如果需要多个格式支持，把这些格式的编码引擎js文件放到后面统统引入进来即可
import 'recorder-core/src/engine/mp3';
import 'recorder-core/src/engine/mp3-engine';
//录制wav格式的用这一句就行
import 'recorder-core/src/engine/wav';

//可选的插件支持项，这个是波形可视化插件
import 'recorder-core/src/extensions/waveview';
import request from "@/utils/request";

import HeadPortrait from "@/components/HeadPortrait";
import Emoji from "@/components/Emoji";
import FileCard from "@/components/FileCard.vue";

export default {
  components: {
    HeadPortrait,
    Emoji,
    FileCard,
  },
  props: {
    frinedInfo: Object,
    default() {
      return {};
    },
  },
  watch: {
    frinedInfo() {
      this.getFriendChatMsg();
    },
  },
  data() {
    return {
      isRecording: false,
      rec: null,
      recBlob: null,
      recordedTime: 0,
      timerId: null,
      chatList: [],
      inputMsg: "",
      showEmoji: false,
      friendInfo: {},
      srcImgList: [],
    };
  },
  mounted() {
    this.recOpen()
    this.reply("你好，我是面试官小陈")
  },
  methods: {
    //回复
    reply(text){
      this.chatList.push({
        headImg: require("@/assets/img/img_2.png"),
        name: "面试官",
        time: this.getNowTime(),
        msg: text,
        chatType: 0, //信息类型，0文字，1图片
        uid: "1002", //uid
      },);
      this.scrollBottom();
      // this.speakText(msg)
    },
    speakText(test) {
      const utterance = new SpeechSynthesisUtterance(test);
      window.speechSynthesis.speak(utterance);
    },
    //打开录音权限
    recOpen() {
      // 创建录音对象
      this.rec = Recorder({
        type: "mp3", // 录音格式，可以换成wav等其他格式
        sampleRate: 16000, // 录音的采样率，越大细节越丰富越细腻
        bitRate: 16, // 录音的比特率，越大音质越好
        onProcess: (buffers, powerLevel, bufferDuration, bufferSampleRate, newBufferIdx, asyncEnd) => {
          // 录音实时回调，大约1秒调用12次本回调
          if (this.wave) this.wave.input(buffers[buffers.length - 1], powerLevel, bufferSampleRate);
        }
      });
      // 打开录音，获得权限
      this.rec.open(() => {
        console.log("录音已打开");
        // if (this.$refs.recwave) {
        //   // 创建音频可视化图形绘制对象
        //   this.wave = Recorder.WaveView({ elem: this.$refs.recwave });
        // }
      }, (msg, isUserNotAllow) => {
        // 用户拒绝了录音权限，或者浏览器不支持录音
        console.log((isUserNotAllow ? "UserNotAllow，" : "") + "无法录音:" + msg);
      });
    },
    //开始录音
    startRecording() {
      if (!this.rec) {
        console.error("未打开录音");
        return;
      }
      this.isRecording = true
      this.rec.start();
      console.log("已开始录音");
      this.stopTimer()
      this.recordedTime = 0
      // 开始计时
      this.startTimer();
    },
    //取消录音
    stopRecording() {
      this.isRecording = false
      this.stopTimer()
    },
    //纶音结束并上传
    saveRecording() {
      if (!this.rec) {
        console.error("未打开录音");
        return;
      }
      this.rec.stop((blob, duration) => {
        // blob就是我们要的录音文件对象，可以上传，或者本地播放
        this.recBlob = blob;
        var localUrl = (window.URL || webkitURL).createObjectURL(blob);
        console.log("录音成功", blob, localUrl, "时长:" + duration + "ms");

        // 发送录音消息
        this.sendAudio(blob, duration);
        // 将录音数据添加到文件列表中
        this.upload(blob); // 把blob文件上传到服务器
        this.isRecording = false
      }, (err) => {
        console.error("结束录音出错：" + err);
        this.rec.close(); // 关闭录音，释放录音资源，当然可以不释放，后面可以连续调用start
        this.rec = null;
      });
    },
    upload(blob) {
      console.log("视频上传服务器：");
      this.blobToDataURI(blob, (result) => {
        request.post('/upload', {
          file: result.split(",")[1],
          format: "wav",
          len: atob(result.split(",")[1]).length,
        })
            .then((res) => {
              console.log(res)
              if (res.code == 200) {
                console.log("返回文字内容：", res.result);
                this.reply(res.result)
                this.speakText(res.result)
              }
            })
            .catch((err) => {
              console.log(err);
            });
      });
    },
    blobToDataURI(blob, callback) {
      var reader = new FileReader();
      reader.readAsDataURL(blob);
      reader.onload = function (e) {
        callback(e.target.result);
      }
    },
    getObjectURL(blob) {
      if (!blob) return '';
      return URL.createObjectURL(blob);
    },
    //录音时间
    startTimer() {
      // 使用 setInterval 来更新 recordedTime
      this.timerId = setInterval(() => {
        this.recordedTime++;
      }, 1000); // 每秒更新一次
    },
    //清除计时器
    stopTimer() {
      // 清除计时器
      clearInterval(this.timerId);
      this.timerId = null;
    },
    // //获取聊天记录
    // getFriendChatMsg() {
    //   let params = {
    //     frinedId: this.frinedInfo.id,
    //   };
    //   getChatMsg(params).then((res) => {
    //     this.chatList = res;
    //     this.chatList.forEach((item) => {
    //       if (item.chatType == 2 && item.extend.imgType == 2) {
    //         this.srcImgList.push(item.msg);
    //       }
    //     });
    //     this.scrollBottom();
    //   });
    // },
    //发送信息
    sendMsg(msgList) {
      this.chatList.push(msgList);
      this.scrollBottom();
    },
    //获取窗口高度并滚动至最底层
    scrollBottom() {
      this.$nextTick(() => {
        const scrollDom = this.$refs.chatContent;
        scrollDom.scrollTop = scrollDom.scrollHeight;
        // animation(scrollDom, scrollDom.scrollHeight - scrollDom.offsetHeight);
      });
    },
    //关闭标签框
    clickEmoji() {
      this.showEmoji = !this.showEmoji;
    },
    // 获取当前的时间
    getNowTime() {
      let dt = new Date()
      let y = dt.getFullYear()
      let mt = (dt.getMonth() + 1).toString().padStart(2, '0')
      let day = dt.getDate().toString().padStart(2, '0')
      let h = dt.getHours().toString().padStart(2, '0')
      let m = dt.getMinutes().toString().padStart(2, '0')
      return y + "-" + mt + "-" + day + " " + h + ":" + m
    },
    //发送文字信息
    sendText() {
      if (this.inputMsg) {
        let chatMsg = {
          headImg: require("@/assets/img/student.png"),
          name: "小白",
          time: this.getNowTime(),
          msg: this.inputMsg,
          chatType: 0, //信息类型，0文字，1图片
          uid: "1001", //uid
        };
        this.sendMsg(chatMsg);
        this.$emit('personCardSort', this.frinedInfo.id)
        this.inputMsg = "";
      } else {
        this.$message({
          message: "消息不能为空哦~",
          type: "warning",
        });
      }
    },
    //发送语音
    sendAudio(blob, duration) {
      // 构造聊天消息对象
      let chatMsg = {
        headImg: require("@/assets/img/student.png"),
        name: "小白", // 发送者名称
        time: this.getNowTime(), // 发送时间，可以自定义时间格式化函数 formatTime()
        msg: "", // 由于是语音消息，msg 可以为空字符串或者特定标识
        chatType: 3, // 信息类型，0文字，1语音
        audioBlob: blob, // 录音文件的 Blob 对象
        uid: "1001", // uid，可以根据实际情况填写
      };

      // 调用发送消息的方法
      this.sendMsg(chatMsg);
    },
    //发送表情
    sendEmoji(msg) {
      let chatMsg = {
        headImg: require("@/assets/img/head_portrait.jpg"),
        name: "大毛是小白",
        time: "09：12 AM",
        msg: msg,
        chatType: 1, //信息类型，0文字，1图片
        extend: {
          imgType: 1, //(1表情，2本地图片)
        },
        uid: "1001",
      };
      this.sendMsg(chatMsg);
      this.clickEmoji();
    },
    //发送本地图片
    sendImg(e) {
      let _this = this;
      console.log(e.target.files);
      let chatMsg = {
        headImg: require("@/assets/img/head_portrait.jpg"),
        name: "大毛是小白",
        time: "09：12 AM",
        msg: "",
        chatType: 1, //信息类型，0文字，1图片, 2文件
        extend: {
          imgType: 2, //(1表情，2本地图片)
        },
        uid: "1001",
      };
      let files = e.target.files[0]; //图片文件名
      if (!e || !window.FileReader) return; // 看是否支持FileReader
      let reader = new FileReader();
      reader.readAsDataURL(files); // 关键一步，在这里转换的
      reader.onloadend = function () {
        chatMsg.msg = this.result; //赋值
        _this.srcImgList.push(chatMsg.msg);
      };
      this.sendMsg(chatMsg);
      e.target.files = null;
    },
    //发送文件
    sendFile(e) {
      let chatMsg = {
        headImg: require("@/assets/img/head_portrait.jpg"),
        name: "大毛是小白",
        time: "09：12 AM",
        msg: "",
        chatType: 2, //信息类型，0文字，1图片, 2文件
        extend: {
          fileType: "", //(1word，2excel，3ppt，4pdf，5zpi, 6txt)
        },
        uid: "1001",
      };
      let files = e.target.files[0]; //图片文件名
      chatMsg.msg = files;
      console.log(files);
      if (files) {
        switch (files.type) {
          case "application/msword":
          case "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            chatMsg.extend.fileType = 1;
            break;
          case "application/vnd.ms-excel":
          case "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
            chatMsg.extend.fileType = 2;
            break;
          case "application/vnd.ms-powerpoint":
          case "application/vnd.openxmlformats-officedocument.presentationml.presentation":
            chatMsg.extend.fileType = 3;
            break;
          case "application/pdf":
            chatMsg.extend.fileType = 4;
            break;
          case "application/zip":
          case "application/x-zip-compressed":
            chatMsg.extend.fileType = 5;
            break;
          case "text/plain":
            chatMsg.extend.fileType = 6;
            break;
          default:
            chatMsg.extend.fileType = 0;
        }
        this.sendMsg(chatMsg);
        e.target.files = null;
      }
    },
    // 发送语音
    telephone() {
      this.$message("该功能还没有开发哦，敬请期待一下吧~🥳");
    },
    //发送视频
    video() {
      this.$message("该功能还没有开发哦，敬请期待一下吧~🥳");
    },
  },
};
</script>

<style lang="scss" scoped>
.chat-window {
  width: 100%;
  height: 100%;
  margin-left: 20px;
  position: relative;

  .top {
    margin-bottom: 50px;

    &::after {
      content: "";
      display: block;
      clear: both;
    }

    .head-pic {
      float: left;
    }

    .info-detail {
      float: left;
      margin: 5px 20px 0;

      .name {
        font-size: 20px;
        font-weight: 600;
        color: #fff;
      }

      .detail {
        color: #9e9e9e;
        font-size: 12px;
        margin-top: 2px;
      }
    }

    .other-fun {
      float: right;
      margin-top: 20px;

      span {
        margin-left: 30px;
        cursor: pointer;
      }

      // .icon-tupian {

      // }
      input {
        display: none;
      }
    }
  }

  .botoom {
    width: 100%;
    height: 75vh;
    background-color: rgb(50, 54, 68);
    border-radius: 20px;
    padding: 20px;
    box-sizing: border-box;
    position: relative;

    .chat-content {
      width: 100%;
      height: 85%;
      overflow-y: scroll;
      padding: 20px;
      box-sizing: border-box;

      &::-webkit-scrollbar {
        width: 0; /* Safari,Chrome 隐藏滚动条 */
        height: 0; /* Safari,Chrome 隐藏滚动条 */
        display: none; /* 移动端、pad 上Safari，Chrome，隐藏滚动条 */
      }

      .chat-wrapper {
        position: relative;
        word-break: break-all;

        .chat-friend {
          width: 100%;
          float: left;
          margin-bottom: 20px;
          display: flex;
          flex-direction: column;
          justify-content: flex-start;
          align-items: flex-start;

          .chat-text {
            max-width: 90%;
            padding: 20px;
            border-radius: 20px 20px 20px 5px;
            background-color: rgb(56, 60, 75);
            color: #fff;

            &:hover {
              background-color: rgb(39, 42, 55);
            }
          }

          .chat-img {
            img {
              width: 100px;
              height: 100px;
            }
          }

          .info-time {
            margin: 10px 0;
            color: #fff;
            font-size: 14px;

            img {
              width: 30px;
              height: 30px;
              border-radius: 50%;
              vertical-align: middle;
              margin-right: 10px;
            }

            span:last-child {
              color: rgb(101, 104, 115);
              margin-left: 10px;
              vertical-align: middle;
            }
          }
        }

        .chat-me {
          width: 100%;
          float: right;
          margin-bottom: 20px;
          position: relative;
          display: flex;
          flex-direction: column;
          justify-content: flex-end;
          align-items: flex-end;

          .chat-text {
            float: right;
            max-width: 90%;
            padding: 20px;
            border-radius: 20px 20px 5px 20px;
            background-color: rgb(29, 144, 245);
            color: #fff;

            &:hover {
              background-color: rgb(26, 129, 219);
            }
          }

          .chat-img {
            img {
              max-width: 300px;
              max-height: 200px;
              border-radius: 10px;
            }
          }

          .info-time {
            margin: 10px 0;
            color: #fff;
            font-size: 14px;
            display: flex;
            justify-content: flex-end;

            img {
              width: 30px;
              height: 30px;
              border-radius: 50%;
              vertical-align: middle;
              margin-left: 10px;
            }

            span {
              line-height: 30px;
            }

            span:first-child {
              color: rgb(101, 104, 115);
              margin-right: 10px;
              vertical-align: middle;
            }
          }
        }
      }
    }

    .chatInputs {
      width: 90%;
      position: absolute;
      bottom: 0;
      margin: 3%;
      display: flex;

      .boxinput {
        width: 50px;
        height: 50px;
        background-color: rgb(66, 70, 86);
        border-radius: 15px;
        border: 1px solid rgb(80, 85, 103);
        position: relative;
        cursor: pointer;

        img {
          width: 30px;
          height: 30px;
          position: absolute;
          left: 50%;
          top: 50%;
          transform: translate(-50%, -50%);
        }
      }

      .emoji {
        transition: 0.3s;

        &:hover {
          background-color: rgb(46, 49, 61);
          border: 1px solid rgb(71, 73, 82);
        }
      }

      .inputs {
        width: 90%;
        height: 50px;
        background-color: rgb(66, 70, 86);
        border-radius: 15px;
        border: 2px solid rgb(34, 135, 225);
        padding: 10px;
        box-sizing: border-box;
        transition: 0.2s;
        font-size: 20px;
        color: #fff;
        font-weight: 100;
        margin: 0 20px;

        &:focus {
          outline: none;
        }
      }

      .send {
        background-color: rgb(29, 144, 245);
        border: 0;
        transition: 0.3s;
        box-shadow: 0px 0px 5px 0px rgba(0, 136, 255);

        &:hover {
          box-shadow: 0px 0px 10px 0px rgba(0, 136, 255);
        }
      }
    }
  }
}
</style>