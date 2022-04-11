<template>
    <div class="chat-container d-flex flex-column">
        <template v-if="doneLoading">
            <ChatHeader v-if="$chatService.state.recipient" :name="$chatService.state.recipient.name"></ChatHeader>
            <ChatBox class="flex-grow-1 overflow-auto"></ChatBox>
            <ChatBar></ChatBar>
        </template>
        <div class="d-flex flex-column h-100 justify-content-center align-items-center" v-else>
            <LoadingSpinner />
        </div>
    </div>
</template>

<script lang="ts">
import ChatBar from "~/components/molecules/ChatBar.vue"
import ChatBox from "~/components/molecules/ChatBox.vue"
import ChatHeader from "~/components/molecules/ChatHeader.vue"
import LoadingSpinner from "~/components/atoms/LoadingSpinner.vue"

export default {
    components: {
        ChatBar,
        ChatBox,
        ChatHeader,
        LoadingSpinner
    },
    data() {
        return {
            doneLoading: false
        }
    },
    watch: {
        '$chatService.state.connected': function (val) {
            setTimeout(() => {
                this.doneLoading = val
            }, 500)
        }
    }
}
</script>

<style scoped>
.chat-container {
    background-color: rgb(240,240,240);
    overflow: none;
}
</style>
