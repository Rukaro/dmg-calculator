import streamlit as st
import numpy as np
import random
import time

# 添加CSS样式
st.markdown("""
<style>
.character-card {
    background-color: #f0f2f6;
    border: 1px solid #ddd;
    border-radius: 10px;
    padding: 15px;
    margin: 5px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.character-card h3 {
    margin-top: 0;
    color: #1f77b4;
    font-size: 16px;
}

.character-card .stats {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.character-card .stat-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.character-card .stat-label {
    font-weight: bold;
    color: #666;
}

.character-card .stat-value {
    background-color: white;
    border: 1px solid #ccc;
    border-radius: 4px;
    padding: 4px 8px;
    min-width: 60px;
    text-align: center;
}

.character-card .power {
    margin-top: 10px;
    padding: 8px;
    background-color: #e8f4fd;
    border-radius: 5px;
    text-align: center;
    font-weight: bold;
    color: #1f77b4;
}

.empty-slot {
    background-color: #f8f9fa;
    border: 2px dashed #ccc;
    border-radius: 10px;
    padding: 30px;
    margin: 5px;
    text-align: center;
    color: #999;
    font-size: 24px;
}

.control-panel {
    background-color: #f8f9fa;
    border: 1px solid #ddd;
    border-radius: 10px;
    padding: 20px;
    margin: 10px 0;
}

.control-panel h3 {
    margin-top: 0;
    color: #333;
    font-size: 18px;
}

.button-group {
    display: flex;
    gap: 10px;
    align-items: center;
    margin: 10px 0;
}

.styled-button {
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 5px;
    padding: 8px 12px;
    cursor: pointer;
    font-size: 16px;
}

.styled-button:hover {
    background-color: #0056b3;
}

.section-header {
    background-color: #e3f2fd;
    border-radius: 8px;
    padding: 10px 15px;
    margin: 15px 0;
    border-left: 4px solid #2196f3;
}

.section-header h2 {
    margin: 0;
    color: #1976d2;
    font-size: 20px;
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

def create_character_card(character, index, side):
    """创建角色卡片HTML"""
    return f"""
    <div class="character-card">
        <h3>{character.name}</h3>
        <div class="stats">
            <div class="stat-row">
                <span class="stat-label">攻击:</span>
                <input type="number" value="{character.attack}" min="100" max="2000" 
                       onchange="updateCharacter('{side}', {index}, 'attack', this.value)" 
                       class="stat-value">
            </div>
            <div class="stat-row">
                <span class="stat-label">防御:</span>
                <input type="number" value="{character.defense}" min="100" max="2000" 
                       onchange="updateCharacter('{side}', {index}, 'defense', this.value)" 
                       class="stat-value">
            </div>
            <div class="stat-row">
                <span class="stat-label">生命:</span>
                <input type="number" value="{character.hp}" min="100" max="6000" 
                       onchange="updateCharacter('{side}', {index}, 'hp', this.value)" 
                       class="stat-value">
            </div>
        </div>
        <div class="power">战力: {character.power:.1f}</div>
    </div>
    """

def create_empty_slot():
    """创建空槽位HTML"""
    return '<div class="empty-slot">➕</div>'

def main():
    st.title("战斗模拟器")
    
    # 初始化session_state
    if 'attacker_count' not in st.session_state:
        st.session_state.attacker_count = 3
    if 'defender_count' not in st.session_state:
        st.session_state.defender_count = 3
    
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
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # 进攻方
        st.markdown('<div class="section-header"><h2>⚔️ 进攻方</h2></div>', unsafe_allow_html=True)
        
        attackers = []
        cols = st.columns(5)
        for i in range(5):
            with cols[i]:
                if i < st.session_state.attacker_count:
                    attack = st.number_input("攻击", 100, 2000, 159, key=f"attacker_attack_{i}")
                    defense = st.number_input("防御", 100, 2000, 215, key=f"attacker_defense_{i}")
                    hp = st.number_input("生命", 100, 6000, 423, key=f"attacker_hp_{i}")
                    
                    char = Character(f"进攻方角色{i+1}", attack, defense, hp)
                    attackers.append(char)
                    
                    # 使用卡片样式显示角色
                    st.markdown(f"""
                    <div class="character-card">
                        <h3>角色 {i+1}</h3>
                        <div class="stats">
                            <div class="stat-row">
                                <span class="stat-label">攻击:</span>
                                <span class="stat-value">{attack}</span>
                            </div>
                            <div class="stat-row">
                                <span class="stat-label">防御:</span>
                                <span class="stat-value">{defense}</span>
                            </div>
                            <div class="stat-row">
                                <span class="stat-label">生命:</span>
                                <span class="stat-value">{hp}</span>
                            </div>
                        </div>
                        <div class="power">战力: {char.power:.1f}</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown('<div class="empty-slot">➕</div>', unsafe_allow_html=True)
        
        # 防守方
        st.markdown('<div class="section-header"><h2>🛡️ 防守方</h2></div>', unsafe_allow_html=True)
        
        defenders = []
        cols = st.columns(5)
        for i in range(5):
            with cols[i]:
                if i < st.session_state.defender_count:
                    attack = st.number_input("攻击", 100, 2000, 159, key=f"defender_attack_{i}")
                    defense = st.number_input("防御", 100, 2000, 215, key=f"defender_defense_{i}")
                    hp = st.number_input("生命", 100, 6000, 423, key=f"defender_hp_{i}")
                    
                    char = Character(f"防守方角色{i+1}", attack, defense, hp)
                    defenders.append(char)
                    
                    # 使用卡片样式显示角色
                    st.markdown(f"""
                    <div class="character-card">
                        <h3>角色 {i+1}</h3>
                        <div class="stats">
                            <div class="stat-row">
                                <span class="stat-label">攻击:</span>
                                <span class="stat-value">{attack}</span>
                            </div>
                            <div class="stat-row">
                                <span class="stat-label">防御:</span>
                                <span class="stat-value">{defense}</span>
                            </div>
                            <div class="stat-row">
                                <span class="stat-label">生命:</span>
                                <span class="stat-value">{hp}</span>
                            </div>
                        </div>
                        <div class="power">战力: {char.power:.1f}</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown('<div class="empty-slot">➕</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="control-panel">', unsafe_allow_html=True)
        
        st.markdown('<h3>🎯 模拟次数</h3>', unsafe_allow_html=True)
        simulation_count = st.number_input("", 1, 10000, 1000, key="simulation_count")
        
        st.markdown('<h3>👥 角色数量</h3>', unsafe_allow_html=True)
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            st.write("**进攻方**")
            if st.button("➕", key="add_attacker", on_click=increase_attackers):
                pass
            if st.button("➖", key="remove_attacker", on_click=decrease_attackers):
                pass
            st.write(f"当前: {st.session_state.attacker_count}")
        
        with col_btn2:
            st.write("**防守方**")
            if st.button("➕", key="add_defender", on_click=increase_defenders):
                pass
            if st.button("➖", key="remove_defender", on_click=decrease_defenders):
                pass
            st.write(f"当前: {st.session_state.defender_count}")
        
        st.markdown('<h3>⚔️ 开始模拟</h3>', unsafe_allow_html=True)
        if st.button("模拟战斗", type="primary", key="start_battle"):
            st.session_state.start_battle = True
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 显示总战力
    attacker_total_power = sum(char.power for char in attackers)
    defender_total_power = sum(char.power for char in defenders)
    
    st.markdown('<div class="section-header"><h2>📊 战力对比</h2></div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.metric("进攻方总战力", f"{attacker_total_power:.1f}")
    with col2:
        st.metric("防守方总战力", f"{defender_total_power:.1f}")
    
    # 战斗结果
    if st.session_state.get('start_battle', False):
        st.markdown('<div class="section-header"><h2>🎯 战斗结果</h2></div>', unsafe_allow_html=True)
        
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