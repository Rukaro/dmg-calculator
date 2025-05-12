import streamlit as st
import numpy as np
import plotly.graph_objects as go

def calculate_old_damage(atk, def_, atk_multiplier):
    return max(0.11 * atk * atk_multiplier - 0.1 * def_, 0) + 70 * atk_multiplier * atk / def_

def calculate_new_damage(atk, def_, atk_multiplier, final_multiplier):
    return (max(0.11 * atk * atk_multiplier - 0.1 * def_, 0) + 70 * atk_multiplier * atk / def_) * final_multiplier

def main():
    st.title("伤害公式对比可视化工具")
    
    # 初始化session_state
    if 'old_multiplier' not in st.session_state:
        st.session_state.old_multiplier = 225
    if 'new_multiplier' not in st.session_state:
        st.session_state.new_multiplier = 78

    # 创建参数调整区域
    col1, col2, col3 = st.columns(3)
    with col1:
        # 使用回调函数更新session_state
        def update_old_value():
            if 'old_input' in st.session_state:
                st.session_state.old_multiplier = st.session_state.old_input
            if 'old_slider' in st.session_state:
                st.session_state.old_multiplier = st.session_state.old_slider

        # 创建控件
        st.slider("旧公式攻击力倍率 (%)", min_value=0, max_value=1000, 
                 value=st.session_state.old_multiplier, step=1, 
                 key="old_slider", on_change=update_old_value)
        st.number_input("", min_value=0, max_value=1000, 
                       value=st.session_state.old_multiplier, step=1, 
                       key="old_input", on_change=update_old_value)
        old_multiplier = st.session_state.old_multiplier / 100

    with col2:
        # 使用回调函数更新session_state
        def update_new_value():
            if 'new_input' in st.session_state:
                st.session_state.new_multiplier = st.session_state.new_input
            if 'new_slider' in st.session_state:
                st.session_state.new_multiplier = st.session_state.new_slider

        # 创建控件
        st.slider("新公式攻击力倍率 (%)", min_value=0, max_value=1000, 
                 value=st.session_state.new_multiplier, step=1, 
                 key="new_slider", on_change=update_new_value)
        st.number_input("", min_value=0, max_value=1000, 
                       value=st.session_state.new_multiplier, step=1, 
                       key="new_input", on_change=update_new_value)
        new_multiplier = st.session_state.new_multiplier / 100

    with col3:
        final_multiplier = st.number_input("新公式最终倍率", min_value=0, max_value=100, value=4, step=1)

    # 创建网格
    atk_range = np.linspace(0, 1000, 100)
    def_range = np.linspace(200, 1000, 100)  # 修改防御力范围
    ATK, DEF = np.meshgrid(atk_range, def_range)

    # 计算伤害差异
    damage_diff = np.zeros_like(ATK)
    for i in range(len(atk_range)):
        for j in range(len(def_range)):
            old_dmg = calculate_old_damage(ATK[i,j], DEF[i,j], old_multiplier)
            new_dmg = calculate_new_damage(ATK[i,j], DEF[i,j], new_multiplier, final_multiplier)
            damage_diff[i,j] = new_dmg - old_dmg

    # 创建热力图
    fig = go.Figure(data=go.Heatmap(
        z=damage_diff,
        x=atk_range,
        y=def_range,
        colorscale='RdBu',
        colorbar=dict(title='伤害差异<br>(新公式 - 旧公式)'),
        zmid=0,
        zmin=-600,  # 限制最小值
        zmax=600    # 限制最大值
    ))

    fig.update_layout(
        title='新旧伤害公式差异热力图',
        xaxis_title='攻击力',
        yaxis_title='防御力',
        height=800,
        width=800
    )

    st.plotly_chart(fig, use_container_width=True)

    # 显示一些统计信息
    st.subheader("统计信息")
    st.write(f"最大伤害差异: {damage_diff.max():.2f}")
    st.write(f"最小伤害差异: {damage_diff.min():.2f}")
    st.write(f"平均伤害差异: {damage_diff.mean():.2f}")

if __name__ == "__main__":
    main() 