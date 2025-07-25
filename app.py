import streamlit as st
import numpy as np
import random
import time

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
}

.character-card h3 {
    margin-top: 0;
    margin-bottom: 15px;
    color: #495057;
    font-size: 16px;
    text-align: center;
}

.attribute-group {
    margin-bottom: 15px;
}

.attribute-label {
    font-weight: bold;
    color: #6c757d;
    margin-bottom: 5px;
}

.attribute-input {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 5px;
}

.attribute-input input {
    flex: 1;
    border: 1px solid #ced4da;
    border-radius: 4px;
    padding: 4px 8px;
    text-align: center;
}

.attribute-input button {
    background-color: #6c757d;
    color: white;
    border: none;
    border-radius: 4px;
    width: 30px;
    height: 30px;
    font-size: 16px;
    cursor: pointer;
}

.attribute-input button:hover {
    background-color: #5a6268;
}

.slider-container {
    margin-top: 5px;
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
</style>
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

def create_character_card(character_index, side, is_active=True):
    """创建角色卡片"""
    if is_active:
        # 获取当前值
        attack_key = f"{side}_attack_{character_index}"
        defense_key = f"{side}_defense_{character_index}"
        hp_key = f"{side}_hp_{character_index}"
        
        attack = st.session_state.get(attack_key, 159)
        defense = st.session_state.get(defense_key, 215)
        hp = st.session_state.get(hp_key, 423)
        
        # 计算战力
        power = 0.35 * attack + 0.28 * defense + 0.14 * hp
        
        return f"""
        <div class="character-card">
            <h3>角色{character_index + 1}</h3>
            <div class="attribute-group">
                <div class="attribute-label">攻击</div>
                <div class="attribute-input">
                    <input type="number" value="{attack}" min="100" max="2000" 
                           onchange="updateValue('{attack_key}', this.value)" />
                    <button onclick="adjustValue('{attack_key}', -1)">-</button>
                    <button onclick="adjustValue('{attack_key}', 1)">+</button>
                </div>
                <div class="slider-container">
                    <input type="range" min="100" max="2000" value="{attack}" 
                           onchange="updateValue('{attack_key}', this.value)" style="width: 100%;" />
                </div>
            </div>
            <div class="attribute-group">
                <div class="attribute-label">防御</div>
                <div class="attribute-input">
                    <input type="number" value="{defense}" min="100" max="2000" 
                           onchange="updateValue('{defense_key}', this.value)" />
                    <button onclick="adjustValue('{defense_key}', -1)">-</button>
                    <button onclick="adjustValue('{defense_key}', 1)">+</button>
                </div>
                <div class="slider-container">
                    <input type="range" min="100" max="2000" value="{defense}" 
                           onchange="updateValue('{defense_key}', this.value)" style="width: 100%;" />
                </div>
            </div>
            <div class="attribute-group">
                <div class="attribute-label">生命</div>
                <div class="attribute-input">
                    <input type="number" value="{hp}" min="100" max="6000" 
                           onchange="updateValue('{hp_key}', this.value)" />
                    <button onclick="adjustValue('{hp_key}', -1)">-</button>
                    <button onclick="adjustValue('{hp_key}', 1)">+</button>
                </div>
                <div class="slider-container">
                    <input type="range" min="100" max="6000" value="{hp}" 
                           onchange="updateValue('{hp_key}', this.value)" style="width: 100%;" />
                </div>
            </div>
        </div>
        """
    else:
        return '<div class="empty-slot">+</div>'

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
    def increase_attackers():
        if st.session_state.attacker_count < 5:
            st.session_state.attacker_count += 1
    
    def decrease_attackers():
        if st.session_state.attacker_count > 1:
            st.session_state.attacker_count -= 1
    
    def increase_defenders():
        if st.session_state.defender_count < 5:
            st.session_state.defender_count += 1
    
    def decrease_defenders():
        if st.session_state.defender_count > 1:
            st.session_state.defender_count -= 1
    
    # 主界面布局
    col1, col2 = st.columns([4, 1])
    
    with col1:
        # 进攻方
        st.markdown('<div class="section-header"><h2>进攻方</h2></div>', unsafe_allow_html=True)
        
        # 创建角色卡片
        cols = st.columns(5)
        for i in range(5):
            with cols[i]:
                if i < st.session_state.attacker_count:
                    # 使用Streamlit组件创建角色卡片
                    st.subheader(f"角色{i+1}")
                    
                    # 攻击
                    attack = st.number_input("攻击", 100, 2000, st.session_state[f'attacker_attack_{i}'], key=f"attacker_attack_{i}")
                    attack_slider = st.slider("", 100, 2000, attack, key=f"attacker_attack_slider_{i}")
                    
                    # 防御
                    defense = st.number_input("防御", 100, 2000, st.session_state[f'attacker_defense_{i}'], key=f"attacker_defense_{i}")
                    defense_slider = st.slider("", 100, 2000, defense, key=f"attacker_defense_slider_{i}")
                    
                    # 生命
                    hp = st.number_input("生命", 100, 6000, st.session_state[f'attacker_hp_{i}'], key=f"attacker_hp_{i}")
                    hp_slider = st.slider("", 100, 6000, hp, key=f"attacker_hp_slider_{i}")
                    
                    # 计算战力
                    power = 0.35 * attack + 0.28 * defense + 0.14 * hp
                    st.write(f"战力: {power:.1f}")
                else:
                    st.markdown('<div class="empty-slot">+</div>', unsafe_allow_html=True)
        
        # 防守方
        st.markdown('<div class="section-header"><h2>防守方</h2></div>', unsafe_allow_html=True)
        
        # 创建角色卡片
        cols = st.columns(5)
        for i in range(5):
            with cols[i]:
                if i < st.session_state.defender_count:
                    # 使用Streamlit组件创建角色卡片
                    st.subheader(f"角色{i+1}")
                    
                    # 攻击
                    attack = st.number_input("攻击", 100, 2000, st.session_state[f'defender_attack_{i}'], key=f"defender_attack_{i}")
                    attack_slider = st.slider("", 100, 2000, attack, key=f"defender_attack_slider_{i}")
                    
                    # 防御
                    defense = st.number_input("防御", 100, 2000, st.session_state[f'defender_defense_{i}'], key=f"defender_defense_{i}")
                    defense_slider = st.slider("", 100, 2000, defense, key=f"defender_defense_slider_{i}")
                    
                    # 生命
                    hp = st.number_input("生命", 100, 6000, st.session_state[f'defender_hp_{i}'], key=f"defender_hp_{i}")
                    hp_slider = st.slider("", 100, 6000, hp, key=f"defender_hp_slider_{i}")
                    
                    # 计算战力
                    power = 0.35 * attack + 0.28 * defense + 0.14 * hp
                    st.write(f"战力: {power:.1f}")
                else:
                    st.markdown('<div class="empty-slot">+</div>', unsafe_allow_html=True)
    
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