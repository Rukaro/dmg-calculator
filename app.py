import streamlit as st
import numpy as np
import random
import time

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
            
            # 随机选择攻击者和目标
            attacker = random.choice(alive_attackers)
            target = random.choice(alive_defenders)
            
            # 计算并造成伤害
            damage = self.calculate_damage(attacker, target)
            target.take_damage(damage)
            
            # 记录战斗日志
            status = "阵亡" if not target.alive else f"剩余生命值: {target.hp:.1f}"
            self.battle_log.append(f"第{round_num}回合: {attacker.name} 攻击 {target.name}，造成 {damage:.1f} 伤害，{target.name} {status}")
            
            round_num += 1
            
            # 防止无限循环
            if round_num > 1000:
                self.battle_log.append("战斗超时，判定为平局")
                return "draw"

def main():
    st.title("战斗模拟器")
    
    # 侧边栏配置
    st.sidebar.header("配置")
    
    # 角色数量设置
    attacker_count = st.sidebar.slider("进攻方角色数量", 1, 5, 3)
    defender_count = st.sidebar.slider("防守方角色数量", 1, 5, 3)
    
    # 模拟次数
    simulation_count = st.sidebar.number_input("模拟战斗次数", 1, 10000, 1000)
    
    # 主界面 - 上下布局
    st.header("进攻方")
    attackers = []
    
    # 创建5个角色槽位
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            if i < attacker_count:
                st.subheader(f"角色 {i+1}")
                attack = st.slider(f"攻击", 100, 2000, 500, key=f"attacker_attack_{i}")
                defense = st.slider(f"防御", 100, 2000, 400, key=f"attacker_defense_{i}")
                hp = st.slider(f"生命", 100, 6000, 1500, key=f"attacker_hp_{i}")
                
                char = Character(f"进攻方角色{i+1}", attack, defense, hp)
                attackers.append(char)
                
                st.write(f"战力: {char.power:.1f}")
            else:
                st.subheader(f"角色 {i+1}")
                st.write("未启用")
    
    st.header("防守方")
    defenders = []
    
    # 创建5个角色槽位
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            if i < defender_count:
                st.subheader(f"角色 {i+1}")
                attack = st.slider(f"攻击", 100, 2000, 450, key=f"defender_attack_{i}")
                defense = st.slider(f"防御", 100, 2000, 500, key=f"defender_defense_{i}")
                hp = st.slider(f"生命", 100, 6000, 1800, key=f"defender_hp_{i}")
                
                char = Character(f"防守方角色{i+1}", attack, defense, hp)
                defenders.append(char)
                
                st.write(f"战力: {char.power:.1f}")
            else:
                st.subheader(f"角色 {i+1}")
                st.write("未启用")
    
    # 显示总战力
    attacker_total_power = sum(char.power for char in attackers)
    defender_total_power = sum(char.power for char in defenders)
    
    st.header("战力对比")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("进攻方总战力", f"{attacker_total_power:.1f}")
    with col2:
        st.metric("防守方总战力", f"{defender_total_power:.1f}")
    
    # 战斗按钮
    if st.button("开始模拟战斗", type="primary"):
        st.header("战斗结果")
        
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

if __name__ == "__main__":
    main() 