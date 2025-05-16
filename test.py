import re

data = '''((FieldLength 30)(FieldWidth 20)(FieldHeight 40)(GoalWidth 2.1)(GoalDepth 0.6)(GoalHeight 0.8)(BorderSize 0)(FreeKickDistance 2)(WaitBeforeKickOff 30)(AgentRadius 0.4)(BallRadius 0.042)(BallMass 0.026)(RuleGoalPauseTime 3)(RuleKickInPauseTime 1)(RuleHalfTime 300)(PassModeMinOppBallDist 1)(PassModeDuration 4)(play_modes BeforeKickOff KickOff_Left KickOff_Right PlayOn KickIn_Left KickIn_Right corner_kick_left corner_kick_right goal_kick_left goal_kick_right offside_left offside_right GameOver Goal_Left Goal_Right free_kick_left free_kick_right direct_free_kick_left direct_free_kick_right pass_left pass_right)(time 27.4004)(half 1)(score_left 0)(score_right 0)(play_mode 0))(RSG 0 1)((nd TRF (SLT 1 0 0 0 0 1 0 0 0 0 1 0 -10 10 10 1)(nd Light (setDiffuse 1 1 1 1) (setAmbient 0.8 0.8 0.8 1) (setSpecular 0.1 0.1 0.1 1)))(nd TRF (SLT 1 0 0 0 0 1 0 0 0 0 1 0 10 -10 10 1)(nd Light (setDiffuse 1 1 1 1) (setAmbient 0 0 0 1) (setSpecular 0.1 0.1 0.1 1)))(nd TRF (SLT -1 -8.74228e-08 -3.82137e-15 0 0 -4.37114e-08 1 0 -8.74228e-08 1 4.37114e-08 -0 0 0 0 1)(nd StaticMesh (setVisible 1) (load models/naosoccerfield.obj) (sSc 2.5 1 2.5)(resetMaterials None_rcs-naofield.png)))(nd TRF (SLT -1 -8.74228e-08 -3.82137e-15 0 0 -4.37114e-08 1 0 -8.74228e-08 1 4.37114e-08 -0 0 0 0 1)(nd StaticMesh (setVisible 1) (load models/skybox.obj) (sSc 10 10 10)(resetMaterials Material_skyrender_0001.tif Material_skyrender_0002.tif Material_skyrender_0003.tif Material_skyrender_0004.tif Material_skyrender_0005.tif Material_skyrender_0006.tif)))(nd TRF (SLT 1 0 0 0 0 1 0 0 0 0 1 0 -15.3 0 0.4 1)(nd TRF (SLT -4.37114e-08 1 4.37114e-08 0 0 -4.37114e-08 1 0 1 4.37114e-08 1.91069e-15 0.3 0 -0.4 1)(nd StaticMesh (setVisible 1) (setTransparent) (load models/leftsoccergoal.obj) (sSc 2.18 0.88 0.68)(resetMaterials naogoalnet yellow)))(nd TRF (SLT 1 0 0 0 0 1 0 0 0 0 1 0 0 -1.07 0 1))(nd TRF (SLT 1 0 0 0 0 1 0 0 0 0 1 0 0 1.07 0 1))(nd TRF (SLT 1 0 0 0 0 1 0 0 0 0 1 0 -0.28 0 0 1))(nd TRF (SLT 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0.42 1))(nd TRF (SLT 1 0 0 0 0 1 0 0 0 0 1 0 0.3 1.05 0.4 1))(nd TRF (SLT 1 0 0 0 0 1 0 0 0 0 1 0 0.3 -1.05 0.4 1)))(nd TRF (SLT -1 -8.74228e-08 -0 -0 8.74228e-08 -1 0 0 0 0 1 0 15.3 0 0.4 1)(nd TRF (SLT -4.37114e-08 1 4.37114e-08 0 0 -4.37114e-08 1 0 1 4.37114e-08 1.91069e-15 0.3 0 -0.4 1)(nd StaticMesh (setVisible 1) (setTransparent) (load models/rightsoccergoal.obj) (sSc 2.18 0.88 0.68)(resetMaterials naogoalnet sky-blue)))(nd TRF (SLT 1 0 0 0 0 1 0 0 0 0 1 0 0 -1.07 0 1))(nd TRF (SLT 1 0 0 0 0 1 0 0 0 0 1 0 0 1.07 0 1))(nd TRF (SLT 1 0 0 0 0 1 0 0 0 0 1 0 -0.28 0 0 1))(nd TRF (SLT 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0.42 1))(nd TRF (SLT 1 0 0 0 0 1 0 0 0 0 1 0 0.3 1.05 0.4 1))(nd TRF (SLT 1 0 0 0 0 1 0 0 0 0 1 0 0.3 -1.05 0.4 1)))(nd TRF (SLT 1 0 0 0 0 1 0 0 0 0 1 0 -24.99 0 0 1)(nd SMN (setVisible 1) (load StdUnitBox) (sSc 1 51 1) (sMat matGrey)))(nd TRF (SLT 1 0 0 0 0 1 0 0 0 0 1 0 24.99 0 0 1)(nd SMN (setVisible 1) (load StdUnitBox) (sSc 1 51 1) (sMat matGrey)))(nd TRF (SLT 1 0 0 0 0 1 0 0 0 0 1 0 0 25 0 1)(nd SMN (setVisible 1) (load StdUnitBox) (sSc 50.98 1 1) (sMat matGrey)))(nd TRF (SLT 1 0 0 0 0 1 0 0 0 0 1 0 0 -25 0 1)(nd SMN (setVisible 1) (load StdUnitBox) (sSc 50.98 1 1) (sMat matGrey)))(nd TRF (SLT 1 0 0 0 0 1 0 0 0 0 1 0 -15 10 0 1))(nd TRF (SLT 1 0 0 0 0 1 0 0 0 0 1 0 -15 -10 0 1))(nd TRF (SLT 1 0 0 0 0 1 0 0 0 0 1 0 15 10 0 1))(nd TRF (SLT 1 0 0 0 0 1 0 0 0 0 1 0 15 -10 0 1))(nd TRF (SLT 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1))(nd TRF (SLT 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1))(nd TRF (SLT 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1))(nd TRF (SLT 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1))(nd TRF (SLT 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1))(nd TRF (SLT 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1))(nd TRF (SLT 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1))(nd TRF (SLT 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1))(nd TRF (SLT 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1))(nd TRF (SLT 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1))(nd TRF (SLT 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1))(nd TRF (SLT 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1))(nd TRF (SLT 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1))(nd TRF (SLT 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1))(nd TRF (SLT 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1))(nd TRF (SLT 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1))(nd TRF (SLT 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1))(nd TRF (SLT 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1))(nd TRF (SLT 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1))(nd TRF (SLT 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1))(nd TRF (SLT 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1))(nd TRF (SLT 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0.0402764 1)(nd StaticMesh (setVisible 1) (load models/soccerball.obj) (sSc 0.042 0.042 0.042)(resetMaterials soccerball_rcs-soccerball.png))))'''

# 提取 play_mode 值
play_mode_match = re.search(r'play_mode\s+(\d+)', data)
play_mode_index = int(play_mode_match.group(1)) if play_mode_match else None

# 提取 play_modes 列表
play_modes_match = re.search(r'play_modes\s+(.*?)$', data)
play_modes_list = play_modes_match.group(1).split() if play_modes_match else []

# 获取实际 playMode 名称
play_mode_name = play_modes_list[play_mode_index] if play_mode_index is not None and play_mode_index < len(play_modes_list) else None

# 提取时间
time_match = re.search(r'time\s+([\d.]+)', data)
time_value = float(time_match.group(1)) if time_match else None

# 提取 score_left
score_left_match = re.search(r'score_left\s+(\d+)', data)
score_left = int(score_left_match.group(1)) if score_left_match else None

# 提取 score_right
score_right_match = re.search(r'score_right\s+(\d+)', data)
score_right = int(score_right_match.group(1)) if score_right_match else None

# 输出结果
print("playMode:", play_mode_name)
print("time:", time_value)
print("score_left:", score_left)
print("score_right:", score_right)