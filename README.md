# Monitoramento de Desempenho de Cruzeiro
Projeto da disciplina de MTP-03 do Instituto Tecnológico de Aeronáutica.

# O que é?
O projeto consiste em um programa que viabiliza análise de estruturas aerodinâmicas e dados de voo em tempo real e de forma dinâmica.<br>
O produto permite o estudo da performance de veículos aéreos em regime de cruzeiro, retornando dados importantes para a avaliação do seu desempenho, de maneira acessível e local, possibilitando agilizar o ciclo de aperfeiçoamento do veículo.

# Dependências
Esse prorama utiliza bibliotecas externas, que precisam ser instaladas para o seu funcionamento adequado.<br>
As bibliotecas utilizadas são:

- dash
- plotly
- pandas
- random

Para instalá-las, basta utilizar um instalador de pacotes:

```sh
# PyPI
pip install 'nome-da-biblioteca'
```

```sh
# conda
conda install -c conda-forge 'nome-da-biblioteca'
```

# Utilização

Ao rodar o arquivo *data-builder.py*, será exibido um endereço para o local-host:

```sh
C:\Users\Usuario\python.exe C:\Users\Usuario\data-builder.py 
Dash is running on http://127.0.0.1:8050/

 * Serving Flask app 'data-builder'
 * Debug mode: on

```
Nesse endereço, é possível encontrar gráficos de performance, bem como caixas para alterar os valores da aeronave:

![alt text](https://github.com/rodrigojamunda82/Projeto-MTP-eVTOL/blob/main/Assets/local-host.png?raw=true)

Os parâmetros são dinâmicos, então não é necessário reiniciar o programa após alterá-los.

# Autores
- João Victor Grigolato Neves
- Johann Finger Knak
- Ricardo Cardoso de Oliveira Filho
- Renan Mariano Machado
- Rodrigo Jamundá Melo
