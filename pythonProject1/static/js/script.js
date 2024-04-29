var banner = document.querySelector('.banner');   //获取可视边框
var imglist = document.querySelector(".imglist");  //获取ul标签
var cir = document.querySelector('.cir');          //获取圆点导航父级div
var lis = imglist.children;                       //所有li标签在一个伪数组中
var thisindex = 0;
var flag = true;

window.onload = function(){
    //由图片width和个数获取ul的width
    imglist.style.width = lis.length*810+'px';      //注意：01width是小写  02不要忘记加单位‘px’

    //根据图片个数添加圆点导航
    for (var i = 0; i < lis.length; i++) {
        var anode = document.createElement('a');    //创建<a></a>
        cir.appendChild(anode);                     //在父级div里面添加<a>
    }

    cir.children[0].classList.add('hover');     //页面必须先存在hover类
    //建立圆点导航anode和ul图片的对应关系
    for(var i=0; i<lis.length; i++){
        cir.children[i].setAttribute('index',i);     //li添加自定义属性'index'
    }

    //圆点点击事件
    cirClick();
    function cirClick(){
        cir.addEventListener('click',function(e){
            if(e.target.nodeName != 'A'){
                return false;
            }
            if(flag){                       //节流阀
                flag = false;
                thisindex = e.target.getAttribute('index');
                // imglist.style.left = -thisindex*610+'px';
                move(imglist,-thisindex*610,function(){
                    flag = true;
                })

                cir.querySelector('.hover').classList.remove('hover');    //恢复在每次点击圆点后原来的样式（由灰变绿）
                e.target.classList.add('hover');                            //圆点点击后样式
            }

        })
    }

    //自动轮播
    auto();
    function auto(){
        setInterval(function(){
            if(flag){
                flag = false;
                if(thisindex == lis.length){
                    thisindex = 0;
                }
                move(imglist,-thisindex*610,function(){
                    flag = true;
                })
                cir.querySelector('.hover').classList.remove('hover');    //恢复在每次点击圆点后原来的样式（由灰变绿）
                cir.children[thisindex].classList.add('hover');
                thisindex++;
            }
        }, 2000);
    }

    //缓动函数
    var num = 0;
    function move(box,target,callback){
        box.myTime = setInterval(function(){
            var osleft = box.offsetLeft;     //这里是属性，不能加()
            var num = (target-osleft) / 10;
            num = num>0 ? Math.ceil(num):Math.floor(num);
            if(osleft == target){
                clearInterval(box.myTime);
                callback && callback();
            }else{
                box.style.left = num+osleft+'px';
            }
        },30)
    }
}