import streamlit as st
import numpy as np
import random
import time

# 设置页面宽度
st.set_page_config(layout="wide")

# 添加CSS样式
st.markdown("""
<style>
.character-card {
    background-color: #f8f9fa;
    border: 1px solid #dee2e6;
    border-radius: 8px;
    padding: 15px;
    margin: 5px;
    min-height: 200px;
    position: relative;
    overflow: hidden;
}

.character-card h3 {
    margin-top: 0;
    margin-bottom: 15px;
    color: #495057;
    font-size: 16px;
    text-align: center;
}

.delete-button {
    position: absolute;
    top: 5px;
    right: 5px;
    background-color: #dc3545;
    color: white;
    border: none;
    border-radius: 50%;
    width: 25px;
    height: 25px;
    font-size: 14px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
}

.delete-button:hover {
    background-color: #c82333;
}

.attribute-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 8px;
}

.attribute-label {
    font-weight: bold;
    color: #495057;
    font-size: 14px;
}

.attribute-value {
    background-color: #f8f9fa;
    border: 1px solid #dee2e6;
    border-radius: 4px;
    padding: 4px 8px;
    min-width: 60px;
    text-align: center;
    font-size: 14px;
    color: #495057;
}

.slider-container {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 15px;
}

.slider-minus {
    background-color: #6c757d;
    color: white;
    border: none;
    border-radius: 4px;
    width: 25px;
    height: 25px;
    font-size: 14px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
}

.slider-minus:hover {
    background-color: #5a6268;
}

.slider-plus {
    background-color: #6c757d;
    color: white;
    border: none;
    border-radius: 4px;
    width: 25px;
    height: 25px;
    font-size: 14px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
}

.slider-plus:hover {
    background-color: #5a6268;
}

.slider {
    flex: 1;
    height: 6px;
    border-radius: 3px;
    background: #e9ecef;
    outline: none;
    -webkit-appearance: none;
}

.slider::-webkit-slider-thumb {
    -webkit-appearance: none;
    appearance: none;
    width: 16px;
    height: 16px;
    border-radius: 50%;
    background: #6c757d;
    cursor: pointer;
}

.slider::-moz-range-thumb {
    width: 16px;
    height: 16px;
    border-radius: 50%;
    background: #6c757d;
    cursor: pointer;
    border: none;
}

.power-display {
    text-align: center;
    font-weight: bold;
    color: #495057;
    margin-top: 10px;
    padding: 5px;
    background-color: #e9ecef;
    border-radius: 4px;
}

.empty-slot {
    background-color: #f8f9fa;
    border: 2px dashed #dee2e6;
    border-radius: 8px;
    padding: 40px 20px;
    margin: 5px;
    text-align: center;
    color: #6c757d;
    font-size: 32px;
    min-height: 200px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: background-color 0.2s;
}

.empty-slot:hover {
    background-color: #e9ecef;
}

.section-header {
    background-color: #e9ecef;
    border-radius: 6px;
    padding: 10px 15px;
    margin: 15px 0;
    border-left: 4px solid #6c757d;
}

.section-header h2 {
    margin: 0;
    color: #495057;
    font-size: 18px;
}

.control-panel {
    background-color: #f8f9fa;
    border: 1px solid #dee2e6;
    border-radius: 8px;
    padding: 20px;
    margin: 10px 0;
    position: sticky;
    top: 20px;
    height: fit-content;
}

.control-panel h3 {
    margin-top: 0;
    margin-bottom: 15px;
    color: #495057;
    font-size: 16px;
}

.simulation-input {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 20px;
}

.simulation-input input {
    flex: 1;
    border: 1px solid #ced4da;
    border-radius: 4px;
    padding: 8px;
    text-align: center;
}

.simulation-input button {
    background-color: #6c757d;
    color: white;
    border: none;
    border-radius: 4px;
    width: 35px;
    height: 35px;
    font-size: 18px;
    cursor: pointer;
}

.simulation-input button:hover {
    background-color: #5a6268;
}

.battle-button {
    background-color: #dc3545;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 12px 24px;
    font-size: 16px;
    font-weight: bold;
    cursor: pointer;
    width: 100%;
}

.battle-button:hover {
    background-color: #c82333;
}

.attribute-section {
    margin-bottom: 15px;
    padding: 8px;
    background-color: white;
    border-radius: 4px;
    border: 1px solid #e9ecef;
}
</style>

<script>
function updateValue(key, value) {
    // 这里需要通过Streamlit的session_state更新值
    // 由于JavaScript无法直接访问Python的session_state，
    // 我们需要通过其他方式处理，比如重新加载页面
    window.location.reload();
}

function adjustValue(key, delta) {
    // 这里需要通过Streamlit的session_state更新值
    // 由于JavaScript无法直接访问Python的session_state，
    // 我们需要通过其他方式处理，比如重新加载页面
    window.location.reload();
}
</script>
""", unsafe_allow_html=True)

class Character:
    def __init__(self, name, attack, defense, hp):
        self.name = name
        self.attack = attack
        self.defense = defense
        self.hp = hp
        self.max_hp = hp
        self.power = 0.35 * attack + 0.28 * defense + 0.14 * hp
        self.alive = True
    
    def take_damage(self, damage):
        self.hp = max(0, self.hp - damage)
        if self.hp <= 0:
            self.alive = False
    
    def heal(self):
        self.hp = self.max_hp
        self.alive = True

class BattleSimulator:
    def __init__(self, attackers, defenders):
        self.attackers = attackers
        self.defenders = defenders
        self.battle_log = []
    
    def calculate_damage(self, attacker, defender):
        base_damage = max(1, attacker.attack * 0.11 - defender.defense * 0.1)
        bonus_damage = 70 * attacker.attack / defender.defense
        return base_damage + bonus_damage
    
    def get_alive_characters(self, team):
        return [char for char in team if char.alive]
    
    def simulate_battle(self):
        # 重置所有角色状态
        for char in self.attackers + self.defenders:
            char.heal()
        
        self.battle_log = []
        round_num = 1
        
        while True:
            alive_attackers = self.get_alive_characters(self.attackers)
            alive_defenders = self.get_alive_characters(self.defenders)
            
            # 检查胜负条件
            if not alive_defenders:
                self.battle_log.append(f"第{round_num}回合: 进攻方获胜！")
                return "attackers"
            if not alive_attackers:
                self.battle_log.append(f"第{round_num}回合: 防守方获胜！")
                return "defenders"
            
            # 进攻方先攻击
            if alive_attackers:
                attacker = random.choice(alive_attackers)
                target = random.choice(alive_defenders)
                damage = self.calculate_damage(attacker, target)
                target.take_damage(damage)
                status = "阵亡" if not target.alive else f"剩余生命值: {target.hp:.1f}"
                self.battle_log.append(f"第{round_num}回合: {attacker.name} 攻击 {target.name}，造成 {damage:.1f} 伤害，{target.name} {status}")
            
            # 检查防守方是否全部阵亡
            alive_defenders = self.get_alive_characters(self.defenders)
            if not alive_defenders:
                self.battle_log.append(f"第{round_num}回合: 进攻方获胜！")
                return "attackers"
            
            # 防守方反击
            if alive_defenders:
                attacker = random.choice(alive_defenders)
                target = random.choice(alive_attackers)
                damage = self.calculate_damage(attacker, target)
                target.take_damage(damage)
                status = "阵亡" if not target.alive else f"剩余生命值: {target.hp:.1f}"
                self.battle_log.append(f"第{round_num}回合: {attacker.name} 反击 {target.name}，造成 {damage:.1f} 伤害，{target.name} {status}")
            
            round_num += 1
            
            # 防止无限循环
            if round_num > 1000:
                self.battle_log.append("战斗超时，判定为平局")
                return "draw"

def main():
    st.title("战斗模拟器")
    
    # 初始化session_state
    if 'attacker_count' not in st.session_state:
        st.session_state.attacker_count = 3
    if 'defender_count' not in st.session_state:
        st.session_state.defender_count = 3
    
    # 初始化角色属性
    for i in range(5):
        for side in ['attacker', 'defender']:
            if f'{side}_attack_{i}' not in st.session_state:
                st.session_state[f'{side}_attack_{i}'] = 159
            if f'{side}_defense_{i}' not in st.session_state:
                st.session_state[f'{side}_defense_{i}'] = 215
            if f'{side}_hp_{i}' not in st.session_state:
                st.session_state[f'{side}_hp_{i}'] = 423
    
    # 角色数量控制函数
    def add_attacker():
        if st.session_state.attacker_count < 5:
            st.session_state.attacker_count += 1
    
    def remove_attacker():
        if st.session_state.attacker_count > 1:
            st.session_state.attacker_count -= 1
    
    def add_defender():
        if st.session_state.defender_count < 5:
            st.session_state.defender_count += 1
    
    def remove_defender():
        if st.session_state.defender_count > 1:
            st.session_state.defender_count -= 1
    
    # 双向同步回调函数
    def sync_attack_slider_to_input():
        for i in range(5):
            if f'attacker_attack_slider_{i}' in st.session_state:
                st.session_state[f'attacker_attack_{i}'] = st.session_state[f'attacker_attack_slider_{i}']
    
    def sync_defense_slider_to_input():
        for i in range(5):
            if f'attacker_defense_slider_{i}' in st.session_state:
                st.session_state[f'attacker_defense_{i}'] = st.session_state[f'attacker_defense_slider_{i}']
    
    def sync_hp_slider_to_input():
        for i in range(5):
            if f'attacker_hp_slider_{i}' in st.session_state:
                st.session_state[f'attacker_hp_{i}'] = st.session_state[f'attacker_hp_slider_{i}']
    
    def sync_defender_attack_slider_to_input():
        for i in range(5):
            if f'defender_attack_slider_{i}' in st.session_state:
                st.session_state[f'defender_attack_{i}'] = st.session_state[f'defender_attack_slider_{i}']
    
    def sync_defender_defense_slider_to_input():
        for i in range(5):
            if f'defender_defense_slider_{i}' in st.session_state:
                st.session_state[f'defender_defense_{i}'] = st.session_state[f'defender_defense_slider_{i}']
    
    def sync_defender_hp_slider_to_input():
        for i in range(5):
            if f'defender_hp_slider_{i}' in st.session_state:
                st.session_state[f'defender_hp_{i}'] = st.session_state[f'defender_hp_slider_{i}']
    
    # 数字输入框同步到滑动条的回调函数
    def sync_input_to_slider(key_prefix):
        for i in range(5):
            if f'{key_prefix}_{i}' in st.session_state:
                slider_key = f'{key_prefix}_slider_{i}'
                if slider_key in st.session_state:
                    st.session_state[slider_key] = st.session_state[f'{key_prefix}_{i}']
    
    def sync_attacker_attack_input_to_slider():
        sync_input_to_slider('attacker_attack')
    
    def sync_attacker_defense_input_to_slider():
        sync_input_to_slider('attacker_defense')
    
    def sync_attacker_hp_input_to_slider():
        sync_input_to_slider('attacker_hp')
    
    def sync_defender_attack_input_to_slider():
        sync_input_to_slider('defender_attack')
    
    def sync_defender_defense_input_to_slider():
        sync_input_to_slider('defender_defense')
    
    def sync_defender_hp_input_to_slider():
        sync_input_to_slider('defender_hp')
    
    # 主界面布局 - 使用更宽的布局
    col1, col2 = st.columns([5, 1])
    
    with col1:
        # 进攻方
        st.markdown('<div class="section-header"><h2>进攻方</h2></div>', unsafe_allow_html=True)
        
        # 创建角色卡片 - 使用简化的Streamlit组件
        cols = st.columns(5)
        for i in range(5):
            with cols[i]:
                if i < st.session_state.attacker_count:
                    # 使用简化的Streamlit组件
                    st.markdown(f'<div class="character-card"><h3>角色{i+1}</h3>', unsafe_allow_html=True)
                    
                    # 攻击
                    st.markdown('<div class="attribute-section">', unsafe_allow_html=True)
                    attack = st.session_state[f'attacker_attack_{i}']
                    st.markdown(f'<div class="attribute-row"><span class="attribute-label">攻击</span><span class="attribute-value">{attack}</span></div>', unsafe_allow_html=True)
                    slider_col1, slider_col2, slider_col3 = st.columns([1, 4, 1])
                    with slider_col1:
                        if st.button("-", key=f"attacker_attack_minus_{i}"):
                            st.session_state[f'attacker_attack_{i}'] = max(100, st.session_state[f'attacker_attack_{i}'] - 1)
                            st.rerun()
                    with slider_col2:
                        st.slider("", 100, 2000, attack, key=f"attacker_attack_slider_{i}", on_change=sync_attack_slider_to_input)
                    with slider_col3:
                        if st.button("+", key=f"attacker_attack_plus_{i}"):
                            st.session_state[f'attacker_attack_{i}'] = min(2000, st.session_state[f'attacker_attack_{i}'] + 1)
                            st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # 防御
                    st.markdown('<div class="attribute-section">', unsafe_allow_html=True)
                    defense = st.session_state[f'attacker_defense_{i}']
                    st.markdown(f'<div class="attribute-row"><span class="attribute-label">防御</span><span class="attribute-value">{defense}</span></div>', unsafe_allow_html=True)
                    slider_col1, slider_col2, slider_col3 = st.columns([1, 4, 1])
                    with slider_col1:
                        if st.button("-", key=f"attacker_defense_minus_{i}"):
                            st.session_state[f'attacker_defense_{i}'] = max(100, st.session_state[f'attacker_defense_{i}'] - 1)
                            st.rerun()
                    with slider_col2:
                        st.slider("", 100, 2000, defense, key=f"attacker_defense_slider_{i}", on_change=sync_defense_slider_to_input)
                    with slider_col3:
                        if st.button("+", key=f"attacker_defense_plus_{i}"):
                            st.session_state[f'attacker_defense_{i}'] = min(2000, st.session_state[f'attacker_defense_{i}'] + 1)
                            st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # 生命
                    st.markdown('<div class="attribute-section">', unsafe_allow_html=True)
                    hp = st.session_state[f'attacker_hp_{i}']
                    st.markdown(f'<div class="attribute-row"><span class="attribute-label">生命</span><span class="attribute-value">{hp}</span></div>', unsafe_allow_html=True)
                    slider_col1, slider_col2, slider_col3 = st.columns([1, 4, 1])
                    with slider_col1:
                        if st.button("-", key=f"attacker_hp_minus_{i}"):
                            st.session_state[f'attacker_hp_{i}'] = max(100, st.session_state[f'attacker_hp_{i}'] - 1)
                            st.rerun()
                    with slider_col2:
                        st.slider("", 100, 6000, hp, key=f"attacker_hp_slider_{i}", on_change=sync_hp_slider_to_input)
                    with slider_col3:
                        if st.button("+", key=f"attacker_hp_plus_{i}"):
                            st.session_state[f'attacker_hp_{i}'] = min(6000, st.session_state[f'attacker_hp_{i}'] + 1)
                            st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # 计算战力
                    power = 0.35 * attack + 0.28 * defense + 0.14 * hp
                    st.markdown(f'<div class="power-display">战力: {power:.1f}</div></div>', unsafe_allow_html=True)
                    
                    # 添加删除按钮（除了第一个角色）
                    if i > 0:
                        if st.button("✕", key=f"remove_attacker_{i}", help="删除此角色"):
                            remove_attacker()
                            st.rerun()
                else:
                    # 空槽位 - 点击添加角色
                    if st.button("+", key=f"add_attacker_slot_{i}", help="添加角色"):
                        add_attacker()
                        st.rerun()
        
        # 防守方
        st.markdown('<div class="section-header"><h2>防守方</h2></div>', unsafe_allow_html=True)
        
        # 创建角色卡片 - 使用简化的Streamlit组件
        cols = st.columns(5)
        for i in range(5):
            with cols[i]:
                if i < st.session_state.defender_count:
                    # 使用简化的Streamlit组件
                    st.markdown(f'<div class="character-card"><h3>角色{i+1}</h3>', unsafe_allow_html=True)
                    
                    # 攻击
                    st.markdown('<div class="attribute-section">', unsafe_allow_html=True)
                    attack = st.session_state[f'defender_attack_{i}']
                    st.markdown(f'<div class="attribute-row"><span class="attribute-label">攻击</span><span class="attribute-value">{attack}</span></div>', unsafe_allow_html=True)
                    slider_col1, slider_col2, slider_col3 = st.columns([1, 4, 1])
                    with slider_col1:
                        if st.button("-", key=f"defender_attack_minus_{i}"):
                            st.session_state[f'defender_attack_{i}'] = max(100, st.session_state[f'defender_attack_{i}'] - 1)
                            st.rerun()
                    with slider_col2:
                        st.slider("", 100, 2000, attack, key=f"defender_attack_slider_{i}", on_change=sync_defender_attack_slider_to_input)
                    with slider_col3:
                        if st.button("+", key=f"defender_attack_plus_{i}"):
                            st.session_state[f'defender_attack_{i}'] = min(2000, st.session_state[f'defender_attack_{i}'] + 1)
                            st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # 防御
                    st.markdown('<div class="attribute-section">', unsafe_allow_html=True)
                    defense = st.session_state[f'defender_defense_{i}']
                    st.markdown(f'<div class="attribute-row"><span class="attribute-label">防御</span><span class="attribute-value">{defense}</span></div>', unsafe_allow_html=True)
                    slider_col1, slider_col2, slider_col3 = st.columns([1, 4, 1])
                    with slider_col1:
                        if st.button("-", key=f"defender_defense_minus_{i}"):
                            st.session_state[f'defender_defense_{i}'] = max(100, st.session_state[f'defender_defense_{i}'] - 1)
                            st.rerun()
                    with slider_col2:
                        st.slider("", 100, 2000, defense, key=f"defender_defense_slider_{i}", on_change=sync_defender_defense_slider_to_input)
                    with slider_col3:
                        if st.button("+", key=f"defender_defense_plus_{i}"):
                            st.session_state[f'defender_defense_{i}'] = min(2000, st.session_state[f'defender_defense_{i}'] + 1)
                            st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # 生命
                    st.markdown('<div class="attribute-section">', unsafe_allow_html=True)
                    hp = st.session_state[f'defender_hp_{i}']
                    st.markdown(f'<div class="attribute-row"><span class="attribute-label">生命</span><span class="attribute-value">{hp}</span></div>', unsafe_allow_html=True)
                    slider_col1, slider_col2, slider_col3 = st.columns([1, 4, 1])
                    with slider_col1:
                        if st.button("-", key=f"defender_hp_minus_{i}"):
                            st.session_state[f'defender_hp_{i}'] = max(100, st.session_state[f'defender_hp_{i}'] - 1)
                            st.rerun()
                    with slider_col2:
                        st.slider("", 100, 6000, hp, key=f"defender_hp_slider_{i}", on_change=sync_defender_hp_slider_to_input)
                    with slider_col3:
                        if st.button("+", key=f"defender_hp_plus_{i}"):
                            st.session_state[f'defender_hp_{i}'] = min(6000, st.session_state[f'defender_hp_{i}'] + 1)
                            st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # 计算战力
                    power = 0.35 * attack + 0.28 * defense + 0.14 * hp
                    st.markdown(f'<div class="power-display">战力: {power:.1f}</div></div>', unsafe_allow_html=True)
                    
                    # 添加删除按钮（除了第一个角色）
                    if i > 0:
                        if st.button("✕", key=f"remove_defender_{i}", help="删除此角色"):
                            remove_defender()
                            st.rerun()
                else:
                    # 空槽位 - 点击添加角色
                    if st.button("+", key=f"add_defender_slot_{i}", help="添加角色"):
                        add_defender()
                        st.rerun()
    
    with col2:
        st.markdown('<div class="control-panel">', unsafe_allow_html=True)
        
        st.markdown('<h3>模拟次数</h3>', unsafe_allow_html=True)
        simulation_count = st.number_input("", 1, 10000, 1000, key="simulation_count")
        
        st.markdown('<h3>模拟战斗</h3>', unsafe_allow_html=True)
        if st.button("模拟战斗", type="primary", key="start_battle"):
            st.session_state.start_battle = True
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 创建角色对象用于战斗
    attackers = []
    for i in range(st.session_state.attacker_count):
        attack = st.session_state[f'attacker_attack_{i}']
        defense = st.session_state[f'attacker_defense_{i}']
        hp = st.session_state[f'attacker_hp_{i}']
        char = Character(f"进攻方角色{i+1}", attack, defense, hp)
        attackers.append(char)
    
    defenders = []
    for i in range(st.session_state.defender_count):
        attack = st.session_state[f'defender_attack_{i}']
        defense = st.session_state[f'defender_defense_{i}']
        hp = st.session_state[f'defender_hp_{i}']
        char = Character(f"防守方角色{i+1}", attack, defense, hp)
        defenders.append(char)
    
    # 显示总战力
    attacker_total_power = sum(char.power for char in attackers)
    defender_total_power = sum(char.power for char in defenders)
    
    st.markdown('<div class="section-header"><h2>战力对比</h2></div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.metric("进攻方总战力", f"{attacker_total_power:.1f}")
    with col2:
        st.metric("防守方总战力", f"{defender_total_power:.1f}")
    
    # 战斗结果
    if st.session_state.get('start_battle', False):
        st.markdown('<div class="section-header"><h2>战斗结果</h2></div>', unsafe_allow_html=True)
        
        # 进度条
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        attacker_wins = 0
        defender_wins = 0
        draws = 0
        
        for i in range(simulation_count):
            # 更新进度
            progress = (i + 1) / simulation_count
            progress_bar.progress(progress)
            status_text.text(f"模拟进度: {i+1}/{simulation_count}")
            
            # 重置随机数种子，确保每次模拟都是独立的
            random.seed(time.time() + i)
            
            # 创建新的模拟器实例
            simulator = BattleSimulator(attackers.copy(), defenders.copy())
            result = simulator.simulate_battle()
            
            if result == "attackers":
                attacker_wins += 1
            elif result == "defenders":
                defender_wins += 1
            else:
                draws += 1
        
        # 显示结果
        st.success("模拟完成！")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("进攻方胜率", f"{attacker_wins/simulation_count*100:.1f}%", f"{attacker_wins}胜")
        with col2:
            st.metric("防守方胜率", f"{defender_wins/simulation_count*100:.1f}%", f"{defender_wins}胜")
        with col3:
            st.metric("平局率", f"{draws/simulation_count*100:.1f}%", f"{draws}平")
        
        # 显示详细统计
        st.subheader("详细统计")
        st.write(f"总模拟次数: {simulation_count}")
        st.write(f"进攻方胜利: {attacker_wins} 次 ({attacker_wins/simulation_count*100:.1f}%)")
        st.write(f"防守方胜利: {defender_wins} 次 ({defender_wins/simulation_count*100:.1f}%)")
        st.write(f"平局: {draws} 次 ({draws/simulation_count*100:.1f}%)")
        
        # 重置状态
        st.session_state.start_battle = False

if __name__ == "__main__":
    main() 