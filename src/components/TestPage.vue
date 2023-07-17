<template>
  <div class="Frame">
    <div class="Frame10">
      <div class="Frame9">
        <span class="Frame9-title">
          정확한 추천을 위해 <br />
          당신에 대해 알려주세요.
        </span>
        <span class="Frame9-sub">
          응답한 기록을 바탕으로 당신에게 꼭 맞는 커피를 추천해드릴께요.
        </span>
        <div
          data-fillout-id="18z1Eu8mDJus"
          data-fillout-embed-type="standard"
          style="width: 100%; height: 1000px"
          data-fillout-inherit-parameters
          data-fillout-dynamic-resize
        ></div>
        <!-- <script src="https://server.fillout.com/embed/v1/"></script> -->
      </div>
    </div>
  </div>
</template>

<script>
export default {
  mounted() {
    const script = document.createElement('script');
    script.src = 'https://server.fillout.com/embed/v1/';
    document.head.appendChild(script);
  },
};
</script>

<style>
.Frame {
  display: flex;
  /* width: 1440px; */
  height: 1200px;
  padding: 0 120px 80px;
  justify-content: center;
  align-items: center;
  gap: 20px;
  background: #fff;
}
.Frame10 {
  display: flex;
  width: 1081px;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 50px;
  flex-shrink: 0;
}
.Frame9 {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 16px;
  align-self: stretch;
}
.Frame9-title {
  width: 923px;
  color: var(--system-grey-900, #212121);
  text-align: center;
  font-family: Inter;
  font-size: 64px;
  font-style: normal;
  font-weight: 700;
  line-height: normal;
  letter-spacing: 2.2px;
  text-transform: uppercase;
}
.Frame9-sub {
  width: 755px;
  color: var(--system-grey-600, #757575);
  text-align: center;
  font-family: Inter;
  font-size: 20px;
  font-style: normal;
  font-weight: 500;
  line-height: normal;
  letter-spacing: 0.2px;
}
</style>
