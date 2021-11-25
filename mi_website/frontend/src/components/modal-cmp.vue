  <template>

      <transition name="modal">

        <div class="modal-mask" @click="close" v-show="show">
          <div class="modal-wrapper">

            <div class="modal-container" @click.stop>


                <slot ></slot>
<!--
              <div class="modal-header">
                <slot name="header">
                  default header
                </slot>
              </div>

              <div class="modal-body">
                <slot name="body">
                  default body
                </slot>
              </div>

              <div class="modal-footer">
                <slot name="footer">
                  default footer
                  <button class="modal-default-button" @click="$emit('close')">
                    OK
                  </button>
                </slot>
              </div>
             -->
            </div>
          </div>
        </div>

      </transition>
    </template>



    <script>
      
    export default {
  name: 'modal',
          delimiters: ['[[', ']]'],
        
        data:function(){return {my:123}},
          props:['show',],
          methods:{
            close:function(){this.$emit('close');},
              saveMe:function(){
                //save logic


                    //var form = this.$refs['__form'];
                    //alert('kk');

                    this.close();
              },
        },
          mounted:function(){
            document.addEventListener("keydown",(e)=>{if(this.show && e.keyCode==27){this.close();}});
          },
      }
      </script>

    <style>
          .modal-mask {
  position: fixed;
  z-index: 9998;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: table;
  transition: opacity 0.3s ease;
}

.modal-wrapper {
  display: table-cell;
  vertical-align: middle;
}

.modal-container {
  width: 90vw;
    max-width: 650px;

  margin: 0px auto;
  padding: 20px 30px;
  background-color: #fff;
  border-radius: 2px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.33);
  transition: all 0.3s ease;
  font-family: Helvetica, Arial, sans-serif;
}

.modal-header h3 {
  margin-top: 0;
  color: #42b983;
}

.modal-body {
    displa:flex;
  margin: 20px 0;
    max-height:350px;
    overflow-y:auto;
}

.modal-default-button {
  float: right;
}

.modal-enter {
  opacity: 0;
}

.modal-leave-active {
  opacity: 0;
}

.modal-enter .modal-container,
.modal-leave-active .modal-container {
  -webkit-transform: scale(1.1);
  transform: scale(1.1);
}
      </style>