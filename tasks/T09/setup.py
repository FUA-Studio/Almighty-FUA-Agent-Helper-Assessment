import os
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, 'work')
for f in ('main.js', 'preload.js', os.path.join('renderer', 'index.html')):
    assert os.path.exists(os.path.join(WORK, f)), f + ' 缺失'
print('T09 环境就绪: ' + WORK + ' (npm install electron 后 npm start 交互复现)')
