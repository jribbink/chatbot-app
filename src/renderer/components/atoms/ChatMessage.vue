<template>
    <div
        class="my-1 d-flex flex-column"
        :class="isSender?'align-items-end':''"
    >
        <div
            class="message"
            :class="isSender?'message-self':'message-recipient'"
            v-html="message.message"
        />
        <span class="pe-2 message-info">
            {{ message.sender.name }} at {{ messageTime }}
        </span>
    </div>
</template>

<script lang="ts">
import Message from "../../models/message"

export default {
    props: {
        message: Message
    },
    computed: {
        messageTime() {
            if(!this.message) return ''
            const hours24 = this.message.date.getHours()
            const hours12 = hours24 % 12
            const minutes = this.message.date.getMinutes()
            const seconds = this.message.date.getSeconds()
            const am = hours24 / 12 < 1

            const minutes_str = String(minutes).padStart(2, '0')
            const seconds_str = String(seconds).padStart(2, '0')

            return `${hours12}:${minutes_str}:${seconds_str} ${am?'AM':'PM'}` 
        },
        isSender() {
            return this.message?.sender.name == this.$chatService.state.self?.name
        }
    }
}
</script>

<style scoped>
.message {
    max-width: 80%;
    padding: 10px;
    border-radius: 5px;
}

.message-self {
    background-color: lightgreen;
}

.message-recipient {
    background-color: lightblue;
}

.message-info {
    font-size: smaller;
}
</style>
