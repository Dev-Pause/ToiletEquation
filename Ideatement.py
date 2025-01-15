#V파이썬으로 아이디어 스케치

Web VPython 3.2
from vpython import *
import random

# 초기 설정
scene = canvas(title='')
ground = box(pos=vector(0, -0.05, 0), size=vector(5, 0.1, 1), color=color.green)  # 땅
radius = 0.1  # 구의 반지름
dt = 0.01  # 시간 간격
fluid_velocity = vector(0.5, 0, 0)  # 유체의 속도
friction_coefficient = 0.1  # 마찰 계수
mass = 1.0  # 구의 질량

# 축구공 생성 (흰색 구)
ball = sphere(pos=vector(0, radius, 0), radius=radius, color=color.white)

# 초기 속도 설정
ball_velocity = vector(0, 0, 0)  # 초기 속도

# 공기 입자 생성
num_layers = 5  # 입자 층 수
particles_per_layer = 100  # 각 층의 입자 수
air_particles = []

# 여러 겹의 입자 생성
for layer in range(num_layers):
    for i in range(particles_per_layer):
        x = random.uniform(-2.5, 2.5)
        y = random.uniform(0.05 + layer * 0.05, 0.15 + layer * 0.05)  # 층별로 높이를 다르게
        z = random.uniform(-0.5, 0.5)
        particle = sphere(pos=vector(x, y, z), radius=0.02, color=color.blue)  # 공기 입자
        particle.velocity = vector(fluid_velocity.x + random.uniform(-0.1, 0.1), fluid_velocity.y, fluid_velocity.z)  # 속도 초기화
        air_particles.append(particle)

# 시뮬레이션 루프
while True:
    rate(100)  # 100프레임/초로 업데이트

    # 공기 입자 위치 업데이트
    for particle in air_particles:
        particle.pos += particle.velocity * dt  # 입자 이동

        # 입자가 구와 충돌하는지 확인
        if mag(particle.pos - ball.pos) < (ball.radius + particle.radius):
            # 충돌 시 반사 처리
            normal = norm(particle.pos - ball.pos)  # 충돌 시 법선 벡터
            particle.velocity = particle.velocity - 2 * dot(particle.velocity, normal) * normal  # 반사

        # 입자가 화면 밖으로 나가면 다시 위치 초기화
        if particle.pos.x > 2.5 or particle.pos.x < -2.5 or particle.pos.z > 0.5 or particle.pos.z < -0.5:
            particle.pos = vector(random.uniform(-2.5, 2.5), random.uniform(0.05, 0.15), random.uniform(-0.5, 0.5))
            particle.velocity = vector(fluid_velocity.x + random.uniform(-0.1, 0.1), fluid_velocity.y, fluid_velocity.z)  # 속도 재설정

    # 유체의 힘 계산 (구에 작용하는 힘)
    force_on_ball = vector(0, 0, 0)
    
    # 유체의 흐름에 의한 힘 (구의 면적과 유체 속도에 비례하여 힘을 가정)
    force_on_ball += vector(fluid_velocity.x, 0, 0) * 0.1  # 힘의 크기를 적절히 조정

    # 마찰력 계산 (구가 굴러가는 것을 고려)
    friction_force = -friction_coefficient * ball_velocity  # 마찰력
    ball_velocity += (force_on_ball + friction_force) / mass * dt  # 마찰력과 힘에 의한 속도 변화

    # 구 위치 업데이트
    ball.pos += ball_velocity * dt
