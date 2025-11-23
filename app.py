import gradio as gr
import random
import time

def game_loop(user_input, history):
    if not user_input:
        return history, gr.update(), gr.update(), gr.update(), ""
    time.sleep(0.6)
    tactician_thought = {
        "status": "Active",
        "analysis": f"Player used '{user_input}'. Pattern match: Balanced.",
        "confidence": round(random.uniform(0.7, 0.98), 2),
        "counter_tactic": "Parry",
    }
    bot_response = f"The Goblin reacts to your '{user_input}' — it shuffles and prepares to counter."
    history.append({"role": "user", "content": user_input})
    history.append({"role": "assistant", "content": bot_response})
    new_player_hp = max(0, random.randint(8, 20))
    new_enemy_hp = max(0, random.randint(5, 20))
    return history, tactician_thought, new_player_hp, new_enemy_hp, ""

custom_css = """
body { background-color: #0b0b0c; color: #e6e6e6; font-family: Inter, Arial, sans-serif; }
.gradio-container { background: transparent !important; padding: 12px; }
#hud-container { background: rgba(255,255,255,0.02); padding:8px 10px; border-radius:8px; margin-bottom:12px; }
"""

with gr.Blocks(title="EvoDungeon") as demo:
    with gr.Row(elem_id="hud-container", variant="panel"):
        with gr.Column(scale=1):
            gr.Markdown("### ⚔️ **EvoDungeon**")
        with gr.Column(scale=2):
            player_hp = gr.Slider(label="Player HP", minimum=0, maximum=20, value=20, interactive=False)
        with gr.Column(scale=0, min_width=40):
            gr.Markdown("### VS")
        with gr.Column(scale=2):
            enemy_hp = gr.Slider(label="Goblin Scout HP", minimum=0, maximum=20, value=20, interactive=False)

    with gr.Row():
        with gr.Column(scale=2):
            chatbot = gr.Chatbot(label="Adventure Log", height=350)
            with gr.Row():
                msg = gr.Textbox(label="Action Input", placeholder="Type an action (e.g., 'I swing my sword')", scale=4, autofocus=True)
                btn = gr.Button("Act", variant="primary", scale=1)

        with gr.Column(scale=1):
            gr.Markdown("### 🔥 Battle Mind")
            brain_output = gr.JSON(value={"status": "Idle", "analysis": "Waiting for input..."}, label="Real-time Analysis")
            gr.Markdown("### 🎒 Inventory")
            gr.Dataframe(
                headers=["Item", "Qty"],
                value=[["Rusty Sword", 1], ["Health Potion", 2], ["Torch", 1]],
                interactive=False,
                row_count=3
            )
            with gr.Accordion("📜 Data Vault ", open=False):
                gr.Markdown("*No vector DB connected*")
                gr.Textbox(value="Goblins fear fire and light.", label="Retrieved Context", interactive=False)

    triggers = [msg.submit, btn.click]
    for trigger in triggers:
        trigger(
            game_loop,
            inputs=[msg, chatbot],
            outputs=[chatbot, brain_output, player_hp, enemy_hp, msg],
        )

if __name__ == "__main__":
    demo.launch(
        theme=gr.themes.Monochrome(radius_size=gr.themes.sizes.radius_md),
        css=custom_css
        #share=True
    )