import json
import os

questions = [
    # CONCEPT 1
    {
        "theme_id": 3,
        "text": "Na avaliação de modelos de extrapolação simples apresentados em gráficos, por que uma série temporal com inúmeras variações ao longo do tempo é considerada menos apropriada para esta metodologia do que uma série com apenas uma quebra acentuada?",
        "image_url": None,
        "general_explanation": "A análise documental indica que a extrapolação simples deve priorizar a parcimônia. Séries com muitas variações exigiriam o uso de múltiplas variáveis dummies para realizar estimativas adequadas, o que compromete a eficiência do modelo.",
        "concept_slug": "dummies-extrapolacao",
        "options": [
            {"text": "Porque demandaria o uso excessivo de várias variáveis dummies para ajustar cada variação, tornando a modelagem excessivamente complexa.", "is_correct": True, "specific_explanation": "O texto explicita que muitas variações requerem uso de várias dummies, o que deve ser evitado."},
            {"text": "Porque a extrapolação simples perde sua capacidade de estimar a constante quando a série apresenta mais de três oscilações.", "is_correct": False, "specific_explanation": "Incorreto. A constante pode ser estimada, mas o modelo perderia parcimônia."},
            {"text": "Porque o coeficiente angular das variáveis dummies anularia automaticamente o efeito sazonal natural das oscilações.", "is_correct": False, "specific_explanation": "Dummies em extrapolação não têm por objetivo anular sazonalidade."},
            {"text": "Porque séries muito voláteis só podem ser tratadas por métodos estocásticos multiplicativos nativos do algoritmo Holt-Winters.", "is_correct": False, "specific_explanation": "Esta justificativa não é a apresentada para a extrapolação simples com dummies."}
        ]
    },
    {
        "theme_id": 3,
        "text": "Ao considerar a reescrita de uma equação de extrapolação simples, a introdução de uma 'dummy' visa fundamentalmente modelar qual fenômeno num gráfico de série temporal?",
        "image_url": None,
        "general_explanation": "Variáveis dummies são adicionadas em extrapolação simples para modelar quebras estruturais, ajustando o intercepto (nível) ou a declividade (inclinação) da série.",
        "concept_slug": "dummies-extrapolacao",
        "options": [
            {"text": "A presença de alterações abruptas ou mudanças duradouras, representadas por interceptos e/ou declividades diferentes.", "is_correct": True, "specific_explanation": "O texto menciona claramente o uso de dummies de intercepto e declividade para representar quebras."},
            {"text": "A decomposição rigorosa da série temporal em fatores sazonais estritos e ruído branco.", "is_correct": False, "specific_explanation": "Decomposição é uma metodologia à parte."},
            {"text": "A substituição estatística de dados perdidos devido a falhas amostrais históricas.", "is_correct": False, "specific_explanation": "Dummies tratam mudanças estruturais, não simplesmente imputam dados perdidos."},
            {"text": "A indução de estacionariedade estrita ao longo de toda a série observada.", "is_correct": False, "specific_explanation": "Dummies não forçam a variância nula característica da estacionariedade pura."}
        ]
    },
    {
        "theme_id": 3,
        "text": "Segundo as considerações sobre modelagem gráfica, qual critério tornou a 'série B' a mais propícia para a reescrita com o uso de dummies de extrapolação?",
        "image_url": None,
        "general_explanation": "A série B detinha uma característica ideal: uma quebra estrutural localizada ao mínimo da série, exigindo o menor número de variáveis dummies para atingir um bom ajuste.",
        "concept_slug": "dummies-extrapolacao",
        "options": [
            {"text": "Apresentava uma quebra bem definida em seu ponto mínimo, o que exigia a introdução do menor número possível de dummies.", "is_correct": True, "specific_explanation": "Exatamente o motivo justificado pela resolução: adequação ótima com mínima inserção de dummies."},
            {"text": "Exibia uma clara sazonalidade nos anos finais que poderia ser facilmente modelada por uma dummy multiplicativa.", "is_correct": False, "specific_explanation": "Sazonalidade nos anos finais era uma característica tratada pela SEL H-W, não pela série B com dummies."},
            {"text": "Mostrava estacionariedade centrada no valor zero desde o início até o fim do período analisado.", "is_correct": False, "specific_explanation": "Se fosse completamente estacionária em zero, indicaria SEL Simples, sem precisar de dummies de extrapolação."},
            {"text": "Demonstrava total ausência de ruído, permitindo a utilização de uma dummy global para toda a extensão dos dados.", "is_correct": False, "specific_explanation": "Não existe dummy global que elimine ruído nesse contexto."}
        ]
    },
    {
        "theme_id": 3,
        "text": "Qual o efeito prático da introdução de inúmeras variáveis dummies em uma equação de extrapolação simples devido a muitas variações ao longo do tempo?",
        "image_url": None,
        "general_explanation": "Ao incluir uma dummy para cada variação, o analista perde graus de liberdade e sobrecarrega a equação, violando o princípio do ajuste ótimo por parcimônia (o uso do menor número de dummies possível).",
        "concept_slug": "dummies-extrapolacao",
        "options": [
            {"text": "Resulta em um sobreajuste onde a complexidade do modelo prejudica a simplicidade analítica procurada pela extrapolação.", "is_correct": True, "specific_explanation": "O texto enfatiza que se deve rever a série buscando o menor número de dummies possível."},
            {"text": "Causa a transformação imediata do modelo em uma Suavização Exponencial de Holt.", "is_correct": False, "specific_explanation": "Modelos não se transformam automaticamente; a abordagem SEL Holt é uma metodologia diferente."},
            {"text": "Garante uma previsão perfeita para curtos períodos devido à eliminação matemática dos resíduos.", "is_correct": False, "specific_explanation": "Muitas dummies não garantem previsão perfeita, apenas forçam o ajuste aos dados passados."},
            {"text": "Desloca o impacto estocástico integralmente para o intercepto da série principal.", "is_correct": False, "specific_explanation": "O impacto estocástico permanece no erro; as dummies ajustam tendências determinísticas."}
        ]
    },
    {
        "theme_id": 3,
        "text": "Um modelo de extrapolação simples que busca ajustar duas fases distintas de crescimento de uma série deve empregar uma dummy associada primariamente a qual parâmetro?",
        "image_url": None,
        "general_explanation": "Fases de crescimento distintas indicam mudanças na inclinação/tendência da curva. Isso é modelado ajustando-se a declividade através de uma dummy de coeficiente angular.",
        "concept_slug": "dummies-extrapolacao",
        "options": [
            {"text": "Ao coeficiente angular, alterando a declividade para refletir a nova taxa de crescimento.", "is_correct": True, "specific_explanation": "Dummies de declividade tratam mudanças na taxa de crescimento da linha de extrapolação."},
            {"text": "Estritamente ao intercepto, elevando a linha paralelamente sem alterar sua inclinação.", "is_correct": False, "specific_explanation": "Mudanças nas taxas de crescimento requerem mudança no coeficiente angular, não apenas no intercepto."},
            {"text": "Ao termo de erro estocástico de forma multiplicativa.", "is_correct": False, "specific_explanation": "Dummies na extrapolação atuam na parte determinística (intercepto/declividade)."},
            {"text": "Ao componente sazonal aditivo referente aos trimestres do ano.", "is_correct": False, "specific_explanation": "Sazonalidade não é o foco principal da extrapolação de quebras de crescimento citadas."}
        ]
    },
    {
        "theme_id": 3,
        "text": "A escolha de não reescrever a equação para séries que não a 'B' baseou-se em qual falha visual nessas outras séries para o método de dummies?",
        "image_url": None,
        "general_explanation": "As demais séries detinham 'muitas variações ao longo do tempo', inviabilizando o tratamento pontual e limpo fornecido por um pequeno número de dummies.",
        "concept_slug": "dummies-extrapolacao",
        "options": [
            {"text": "Apresentavam sucessivas e constantes variações ao longo do período, distanciando-se de uma quebra pontual bem demarcada.", "is_correct": True, "specific_explanation": "O documento ressalta que as demais possuíam muitas variações, exigindo várias variáveis dummies."},
            {"text": "Possuíam comportamento estritamente constante e horizontal, tornando o intercepto irrelevante.", "is_correct": False, "specific_explanation": "Isso descreve a série C (SEL Simples), não o problema relatado com as séries com muitas variações."},
            {"text": "Sofriam forte influência do componente multiplicativo sazonal não tratável pela matemática da extrapolação.", "is_correct": False, "specific_explanation": "A razão explícita era a quantidade de variações contínuas, não necessariamente sazonalidade não tratável."},
            {"text": "Estavam limitadas a amostras com observações anuais, impossibilitando dummies mensais.", "is_correct": False, "specific_explanation": "O horizonte temporal das amostras não foi o motivo citado na resolução."}
        ]
    },
    {
        "theme_id": 3,
        "text": "Se a extrapolação simples for conduzida sem o uso de dummies numa série que possui uma quebra de intercepto bem no meio da amostra, o que tenderá a ocorrer com a linha ajustada?",
        "image_url": None,
        "general_explanation": "Uma única linha ajustada a uma série com quebra de nível passará pelo meio dos dois patamares, não representando fielmente nem o período anterior nem o posterior à quebra.",
        "concept_slug": "dummies-extrapolacao",
        "options": [
            {"text": "Ela apresentará um mau ajuste geral, errando sistematicamente antes e depois da quebra por não capturar o salto de nível.", "is_correct": True, "specific_explanation": "Ao ignorar a quebra, a linha ajustada sofre distorções para tentar balancear os erros dos dois regimes distintos."},
            {"text": "Ela se ajustará perfeitamente apenas ao último trecho, ignorando os dados do primeiro trecho por conta dos mínimos quadrados.", "is_correct": False, "specific_explanation": "O método de estimação clássica considera todos os pontos, não apenas os recentes."},
            {"text": "Ela irá gerar estimativas de erro nulo, pois o algoritmo suaviza quebras independentemente da presença de dummies.", "is_correct": False, "specific_explanation": "Extrapolação não suaviza falhas automaticamente; isso é papel da Suavização Exponencial (SEL)."},
            {"text": "Ela indicará que o componente de tendência é zero, gerando previsões horizontais a partir da quebra.", "is_correct": False, "specific_explanation": "A linha ainda terá alguma inclinação, apenas estará muito desajustada da realidade dos dados."}
        ]
    },
    {
        "theme_id": 3,
        "text": "A inclusão de uma variável dummy na modelagem por extrapolação atua sobre a equação determinística de que forma?",
        "image_url": None,
        "general_explanation": "Ela permite a criação de equações segmentadas no tempo, alterando o intercepto ou declividade (coeficiente angular) a partir de um instante t predefinido.",
        "concept_slug": "dummies-extrapolacao",
        "options": [
            {"text": "Permitindo a flexibilização do intercepto e da declividade, criando sub-regimes dentro da trajetória da série analisada.", "is_correct": True, "specific_explanation": "Este é exatamente o papel teórico da dummy na extrapolação de tendências segmentadas."},
            {"text": "Atribuindo pesos que decaem exponencialmente para as observações mais antigas da série temporal.", "is_correct": False, "specific_explanation": "Esta é a definição de suavização exponencial, não de modelagem determinística com dummy."},
            {"text": "Acelerando os cálculos do método SEATS ao converter os resíduos para um modelo ARIMA.", "is_correct": False, "specific_explanation": "A dummy em extrapolação não possui relação com os algoritmos ARIMA/SEATS de decomposição."},
            {"text": "Alterando retroativamente a escala da série para que esta seja compatível com distribuições log-normais.", "is_correct": False, "specific_explanation": "A dummy modela quebras aditivas ou multiplicativas de forma direta, não altera distribuições estatísticas prévias."}
        ]
    },
    {
        "theme_id": 3,
        "text": "Quando um analista detecta uma 'quebra ao mínimo da série', a recomendação do gabarito é introduzir uma dummy para ajustar a equação. Que componente visual do gráfico corrobora essa necessidade?",
        "image_url": None,
        "general_explanation": "A presença de um ponto de inflexão claro (onde a direção ou nível da série muda abruptamente, gerando o formato em 'V' ou similar) indica uma única e forte quebra estrutural justificando a dummy.",
        "concept_slug": "dummies-extrapolacao",
        "options": [
            {"text": "A visualização de uma inflexão proeminente ou mudança de trajetória após o ponto de mínimo, sem oscilações drásticas excessivas subsequentes.", "is_correct": True, "specific_explanation": "A adequação da série 'B' ocorreu porque havia uma quebra clara sem as múltiplas oscilações difusas vistas nas outras."},
            {"text": "A presença contínua de picos e vales regulares em cada trimestre que formam múltiplos mínimos anuais.", "is_correct": False, "specific_explanation": "Isso descreveria sazonalidade tratável por Holt-Winters, não uma única quebra tratável por uma dummy na extrapolação."},
            {"text": "O gráfico apresentando uma reta horizontal permanente próxima de zero sem qualquer desvio visual.", "is_correct": False, "specific_explanation": "Isso caracterizaria a SEL Simples pela total ausência de tendência ou quebra."},
            {"text": "O isolamento absoluto de todos os componentes de erro num quadrante separado do gráfico principal.", "is_correct": False, "specific_explanation": "Essa divisão não é a motivação visual para inserir uma dummy de quebra estrutural."}
        ]
    },
    {
        "theme_id": 3,
        "text": "Em resumo, qual é a principal condição imposta pelas considerações do texto para o uso vantajoso das variáveis dummies num modelo de extrapolação simples?",
        "image_url": None,
        "general_explanation": "A regra de ouro é a parcimônia: as dummies são vantajosas apenas se o ajuste perfeito for alcançado com o menor número delas possível; muitas variações descartam o método.",
        "concept_slug": "dummies-extrapolacao",
        "options": [
            {"text": "Deve-se obter um modelo em que a equação melhor se ajuste através do menor número de dummies possível.", "is_correct": True, "specific_explanation": "A resposta repete as palavras do documento original: o menor número possível e o melhor ajuste."},
            {"text": "A série temporal deve ser estritamente decrescente para que o intercepto dummy assuma valores negativos válidos.", "is_correct": False, "specific_explanation": "A direção da série não invalida o uso das dummies."},
            {"text": "É imperativo que a série contenha evidências de sazonalidade forte e contínua para validar o uso de variáveis temporais.", "is_correct": False, "specific_explanation": "Sazonalidade orientaria o uso de SEL Holt-Winters ou métodos sazonais clássicos, não necessariamente dummies em extrapolação focado em quebras de nível."},
            {"text": "A metodologia deve ser sempre associada à estimação X13-ARIMA em segundo plano para suavizar o componente de tendência.", "is_correct": False, "specific_explanation": "Não há obrigatoriedade de associação com X13-ARIMA para usar extrapolação clássica."}
        ]
    },

    # CONCEPT 2
    {
        "theme_id": 3,
        "text": "Ao analisar a série rotulada como 'A', identificou-se visualmente a presença de tendência geral aliada, nos anos finais, a movimentos sazonais. Diante disso, qual metodologia SEL foi recomendada?",
        "image_url": None,
        "general_explanation": "A combinação de tendência (crescimento ou decrescimento de longo prazo) e sazonalidade (padrão cíclico regular, notado nos anos finais) indica a metodologia SEL Holt-Winters.",
        "concept_slug": "identificacao-sel",
        "options": [
            {"text": "Suavização Exponencial Linear Holt-Winters (SEL H-W).", "is_correct": True, "specific_explanation": "Conforme o gabarito, a série 'A' possui tendência e sazonalidade nos anos finais, exigindo SEL H-W."},
            {"text": "Suavização Exponencial Linear de Winters (SEL Winters) pura.", "is_correct": False, "specific_explanation": "SEL Winters pura foi reservada pelo autor para a série com tendência mas sem sazonalidade visual expressa."},
            {"text": "Suavização Exponencial Simples (SEL Simples).", "is_correct": False, "specific_explanation": "A SEL Simples é indicada para a ausência de tendência e de sazonalidade."},
            {"text": "Metodologia SEATS baseada em componentes estocásticos sazonais.", "is_correct": False, "specific_explanation": "O comando pedia a escolha entre metodologias de Suavização Exponencial Linear explanadas."}
        ]
    },
    {
        "theme_id": 3,
        "text": "A série 'B' apresenta variações para cima e para baixo e se mostra 'estacionária em torno do valor zero', no entanto, a análise afirma que ela detém claramente tendência. Baseado nisto, qual metodologia SEL é a indicada?",
        "image_url": None,
        "general_explanation": "Apesar do comportamento de oscilações ao longo da linha zero (sugerindo sub-estacionariedade), a detecção global de uma tendência orienta a classificação para SEL Winters, de acordo com o documento.",
        "concept_slug": "identificacao-sel",
        "options": [
            {"text": "SEL Winters.", "is_correct": True, "specific_explanation": "A resposta do gabarito especifica textualmente que a série B 'detém tendência, portanto seria SEL Winters'."},
            {"text": "SEL Simples.", "is_correct": False, "specific_explanation": "A presença clara da tendência desqualifica a SEL Simples."},
            {"text": "SEL Holt-Winters.", "is_correct": False, "specific_explanation": "A falta de sazonalidade declarada impede a classificação como Holt-Winters pleno."},
            {"text": "Extrapolação Simples estrita sem correção sazonal.", "is_correct": False, "specific_explanation": "A questão demandava especificamente metodologias de Suavização Exponencial Linear."}
        ]
    },
    {
        "theme_id": 3,
        "text": "Qual das características abaixo foi determinante para definir a aplicação da metodologia 'SEL Simples' à série 'C'?",
        "image_url": None,
        "general_explanation": "A SEL Simples é adequada quando a série é um comportamento de oscilação aleatória estável, ou seja, está claramente centrada em um valor (como zero) e não detém nem tendência nem sazonalidade.",
        "concept_slug": "identificacao-sel",
        "options": [
            {"text": "A série estar centrada no valor zero e não apresentar nem tendência direcional nem movimentos sazonais.", "is_correct": True, "specific_explanation": "O gabarito explicita: 'A série está claramente centrada no valor zero e não detém nem tendência nem sazonalidade, então... SEL simples'."},
            {"text": "A identificação de uma forte correlação serial nos anos iniciais seguida de alta volatilidade e sazonalidade.", "is_correct": False, "specific_explanation": "Isto demandaria SEL H-W ou uma modelagem mais complexa."},
            {"text": "O fato de a série demandar uma grande quantidade de dummies de intercepto e declividade.", "is_correct": False, "specific_explanation": "O uso de dummies refere-se à extrapolação simples, não ao algoritmo SEL Simples."},
            {"text": "A presença de uma componente tendencial puramente negativa sem ciclos periódicos associados.", "is_correct": False, "specific_explanation": "Uma componente tendencial (positiva ou negativa) demandaria o uso de SEL Holt ou SEL Winters."}
        ]
    },
    {
        "theme_id": 3,
        "text": "Considerando as regras de identificação visual, a ausência de um comportamento repetitivo em espaçamentos de tempo fixos (como meses ou trimestres) implica a não utilização de qual componente de equação SEL?",
        "image_url": None,
        "general_explanation": "O comportamento repetitivo em tempos fixos define a sazonalidade. Sem sazonalidade, descarta-se o algoritmo SEL Holt-Winters completo em favor de Holt/Winters (só tendência) ou Simples (nenhum).",
        "concept_slug": "identificacao-sel",
        "options": [
            {"text": "A componente que trata as variações periódicas, desabilitando o uso da modelagem sazonal da SEL Holt-Winters.", "is_correct": True, "specific_explanation": "A ausência de padrão sazonal leva à exclusão da metodologia Holt-Winters (focada em sazonalidade)."},
            {"text": "A constante de intercepto basal exigida na SEL Simples para amortecer as flutuações centradas no zero.", "is_correct": False, "specific_explanation": "A ausência de sazonalidade não tem impacto direto na eliminação do nível ou da constante de base."},
            {"text": "O modelo auto-regressivo de médias móveis do método SEATS integrado às previsões de longo prazo.", "is_correct": False, "specific_explanation": "SEATS não é um método SEL clássico mencionado nas opções de suavização."},
            {"text": "A ponderação estocástica que define o caminho determinístico da série na metodologia Winters clássica.", "is_correct": False, "specific_explanation": "O decaimento exponencial dos pesos acontece em todas as metodologias SEL."}
        ]
    },
    {
        "theme_id": 3,
        "text": "Se a série 'A' não demonstrasse visualmente a sazonalidade nos anos finais e apresentasse apenas a sua nítida linha de trajetória de crescimento, como ela deveria ser reclassificada segundo a lógica aplicada?",
        "image_url": None,
        "general_explanation": "Uma série com apenas tendência (crescimento claro) e nenhuma sazonalidade observável é classicamente adequável ao método SEL Winters (ou Holt) na terminologia apresentada.",
        "concept_slug": "identificacao-sel",
        "options": [
            {"text": "Deveria ser classificada para a metodologia SEL Winters, pois reteria sua tendência sem incorporar sazonalidade.", "is_correct": True, "specific_explanation": "A lógica do documento associa tendência exclusiva à aplicação de SEL Winters."},
            {"text": "Deveria ser remanejada para a metodologia SEL Simples, assumindo-se que a tendência de longo prazo seja estocástica.", "is_correct": False, "specific_explanation": "A SEL Simples pressupõe ausência de tendência visível."},
            {"text": "Manteria a classificação SEL Holt-Winters por medida de conservadorismo estatístico de longo prazo.", "is_correct": False, "specific_explanation": "Sem sazonalidade, as equações de Holt-Winters adicionariam complexidade indesejada."},
            {"text": "Seria obrigatoriamente convertida para uma Decomposição clássica sem suavização adaptativa.", "is_correct": False, "specific_explanation": "A questão aborda a reclassificação dentro das opções de metodologias SEL."}
        ]
    },
    {
        "theme_id": 3,
        "text": "Na descrição da série 'B', a observação de 'pequenas variações para cima ou para baixo' em torno do zero entra em aparente conflito visual com qual componente que garantiu a escolha pela SEL Winters?",
        "image_url": None,
        "general_explanation": "Embora a série oscile em torno do zero de forma estacionária aparente em nível micro, no nível macro (longo prazo), ela 'claramente detém tendência', sendo esta a justificativa para a SEL Winters.",
        "concept_slug": "identificacao-sel",
        "options": [
            {"text": "A presença global e inegável de uma tendência que subjaz às pequenas flutuações estacionárias locais.", "is_correct": True, "specific_explanation": "Apesar das pequenas flutuações em torno do zero, a forte evidência de tendência direcional exigiu o método SEL Winters."},
            {"text": "A constatação de múltiplos padrões sazonais ocultos causados pelas variações locais em torno do zero.", "is_correct": False, "specific_explanation": "Sazonalidade levaria a SEL H-W, o que não foi o caso da série B."},
            {"text": "A completa falta de estacionariedade que invalidou o uso da SEL Simples.", "is_correct": False, "specific_explanation": "O texto afirma que ela possui alguma estacionariedade em torno de zero, mas a tendência se impôs."},
            {"text": "A aplicação forçada do filtro de médias móveis do X13-ARIMA que gerou as pequenas oscilações.", "is_correct": False, "specific_explanation": "Não há menção ao uso do X13 para causar variações visuais no contexto da identificação gráfica para SEL."}
        ]
    },
    {
        "theme_id": 3,
        "text": "A série 'C' foi diagnosticada sem tendência nem sazonalidade. Num contexto de estimativas futuras reais utilizando a SEL Simples aplicada a ela, que comportamento se espera da linha de previsão?",
        "image_url": None,
        "general_explanation": "A metodologia SEL Simples estima o nível da série sem taxas de crescimento ou decrescimento. Consequentemente, suas previsões futuras tendem a ser representadas por uma linha constante plana.",
        "concept_slug": "identificacao-sel",
        "options": [
            {"text": "As previsões se estabilizarão em uma linha constante, refletindo a premissa de um nível permanente sem inclinações sazonais ou de tendência.", "is_correct": True, "specific_explanation": "Um dos princípios da previsão da SEL Simples é o delineamento de estimativas futuras como uma reta horizontal a partir da última suavização."},
            {"text": "As previsões exibirão crescimento aditivo contínuo de forma a acompanhar variações estocásticas.", "is_correct": False, "specific_explanation": "Isso caracterizaria previsões do método de Holt ou Holt-Winters."},
            {"text": "A linha de previsão oscilará bruscamente, simulando os ruídos aleatórios observados em torno da constante zero.", "is_correct": False, "specific_explanation": "O objetivo da suavização é retirar os ruídos, entregando uma estimativa base limpa (constante)."},
            {"text": "As previsões decairão a zero exponencialmente à medida que a influência sazonal recua num modelo multiplicativo.", "is_correct": False, "specific_explanation": "Decaimento exponencial de previsão não é a saída típica da SEL Simples em séries estacionárias."}
        ]
    },
    {
        "theme_id": 3,
        "text": "Qual o risco principal de se utilizar de forma negligente a metodologia SEL Simples em uma série semelhante à 'A' (com tendência e sazonalidade evidentes)?",
        "image_url": None,
        "general_explanation": "A SEL Simples ignoraria completamente o vetor de crescimento constante (tendência) e os padrões periódicos, resultando em fortes atrasos sistemáticos nos ajustes e previsões muito distantes da realidade observada nos ciclos.",
        "concept_slug": "identificacao-sel",
        "options": [
            {"text": "A incapacidade de capturar direcionalidade e movimentos periódicos causaria erros crônicos de previsão, que tratariam as elevações reais como se fossem apenas erros temporários.", "is_correct": True, "specific_explanation": "A metodologia SEL Simples forçaria uma média de nível e subestimaria o crescimento da série 'A'."},
            {"text": "O método provocaria uma amplificação do ruído sazonal ao tentar amortecer a tendência estocástica inerente aos dados.", "is_correct": False, "specific_explanation": "A SEL Simples sequer possui mecanismo para amplificar ou modelar efeitos sazonais ativamente."},
            {"text": "A aplicação provocaria o travamento estatístico devido à explosão da variância em séries com tendência multiplicativa.", "is_correct": False, "specific_explanation": "Embora o erro preditivo seria grande, não há explosão matemática inerente do cálculo simples, apenas imprecisão extrema."},
            {"text": "Os pesos atribuídos a observações antigas seriam zerados automaticamente, tornando a estimativa idêntica a uma Extrapolação Simples com dummies.", "is_correct": False, "specific_explanation": "Os métodos operam de forma distinta e pesos não seriam cortados, o decaimento é gradual."}
        ]
    },
    {
        "theme_id": 3,
        "text": "A distinção entre SEL Winters e SEL Holt-Winters na análise gráfica oferecida no documento se reduz estritamente à presença de qual tipo de comportamento na série histórica?",
        "image_url": None,
        "general_explanation": "A diferença repousa na constatação visual da sazonalidade (como notado nos anos finais da série A), o que obriga a mudança de um modelo focado apenas em tendência (Winters/Holt) para o completo (H-W).",
        "concept_slug": "identificacao-sel",
        "options": [
            {"text": "O comportamento repetitivo periódico em determinados intervalos de tempo, tipicamente caracterizado como sazonalidade.", "is_correct": True, "specific_explanation": "Sazonalidade é o fator extra que transforma a recomendação em SEL Holt-Winters (em oposição a SEL Winters)."},
            {"text": "As sub-estacionariedades locais que oscilam agressivamente na vizinhança da marca zero do gráfico.", "is_correct": False, "specific_explanation": "Essa característica indicava a estacionariedade presente na série B, mas não foi a divisora de águas principal entre Winters e Holt-Winters."},
            {"text": "O declive direcional generalizado focado exclusivamente na variação do intercepto nos últimos cinco anos da série.", "is_correct": False, "specific_explanation": "A variação de intercepto e declive generalizado seria tendência pura, comum a ambos os métodos com componente trend."},
            {"text": "As quebras estruturais agudas que invalidam qualquer possibilidade de estimação via métodos adaptativos contínuos.", "is_correct": False, "specific_explanation": "Se a série tivesse esse comportamento severo, as metodologias de decomposição ou dummies seriam sugeridas, em vez dos métodos SEL clássicos."}
        ]
    },
    {
        "theme_id": 3,
        "text": "Tendo em conta as metodologias apresentadas, a necessidade técnica que obriga o analista a recorrer à observação gráfica antes da escolha do modelo SEL se deve a:",
        "image_url": None,
        "general_explanation": "A observação gráfica permite a identificação clara e intuitiva dos componentes estruturais fundamentais dos dados, como tendência macro e padrões sazonais (ou sua ausência), vitais para determinar a equação adequada.",
        "concept_slug": "identificacao-sel",
        "options": [
            {"text": "Permitir o diagnóstico direto sobre a existência de tendência, sazonalidade ou centragem, garantindo que o algoritmo de suavização escolhido conte com os componentes apropriados.", "is_correct": True, "specific_explanation": "A observação gráfica ditou o gabarito das séries A, B e C, classificando com exatidão a presença ou não de tendência e sazonalidade."},
            {"text": "Fornecer uma prova visual de que métodos não-estocásticos falham inexoravelmente perante correlações temporais longas observadas em dados reais.", "is_correct": False, "specific_explanation": "O objetivo não é invalidar métodos, mas sim direcionar qual metodologia SEL específica aplicar com base nos componentes visualizados."},
            {"text": "Validar a normalidade multivariada dos resíduos exigida rigorosamente pelos estimadores de Decomposição clássica presentes em algoritmos SEL.", "is_correct": False, "specific_explanation": "Métodos SEL não impõem suposições rígidas prévias de normalidade multivariada dos resíduos para sua mera seleção visual."},
            {"text": "Garantir que não haja nenhuma dummy omitida que possa invalidar as estimativas finais dos interceptos locais do algoritmo.", "is_correct": False, "specific_explanation": "Dummies são tema da extrapolação simples, enquanto o foco aqui é a seleção da metodologia de suavização."}
        ]
    },

    # CONCEPT 3
    {
        "theme_id": 3,
        "text": "Comparando as estimativas de Decomposição utilizando os pacotes SEATS e X13-ARIMA no RStudio, qual é a base primária da abordagem utilizada pelo filtro X11/X13-ARIMA para o desmembramento de uma série?",
        "image_url": None,
        "general_explanation": "O método X11 (e sua evolução X13-ARIMA) tem seu núcleo original fortemente centrado no uso sequencial de filtros baseados em médias móveis associado à modelagem ARIMA para projetar e corrigir os extremos.",
        "concept_slug": "decomposicao-seats-x13",
        "options": [
            {"text": "A aplicação de filtros iterativos fundamentados no uso de médias móveis.", "is_correct": True, "specific_explanation": "A resposta fornecida na prova afirma textualmente que a estimativa X11 ou X13-Arima utiliza médias móveis para estimar os componentes."},
            {"text": "A construção de modelos unicamente determinísticos de Suavização Exponencial Holt-Winters aditiva.", "is_correct": False, "specific_explanation": "O X11 não tem por base a formulação da suavização exponencial SEL."},
            {"text": "O enquadramento da série temporal através de extrapolação simples estrita sem intervenção humana.", "is_correct": False, "specific_explanation": "Extrapolação simples e Decomposição via médias móveis (X11) são abordagens distintas."},
            {"text": "A regressão pura por mínimos quadrados ordinários visando exclusão estocástica dos erros.", "is_correct": False, "specific_explanation": "O X11 utiliza médias móveis, não minimização quadrática de regressões estritas OLS para extrair sazonalidade."}
        ]
    },
    {
        "theme_id": 3,
        "text": "Diferentemente do modelo associado ao X13-ARIMA, a metodologia subjacente original empregada pelo método de decomposição SEATS fundamenta-se integralmente em que tipo de base?",
        "image_url": None,
        "general_explanation": "Enquanto o X13 advém do uso de médias móveis complementadas pelo ARIMA, o método SEATS já foi concebido estruturalmente como uma metodologia orientada a sinais estocásticos puros (ARIMA model-based).",
        "concept_slug": "decomposicao-seats-x13",
        "options": [
            {"text": "Uma fundamentação em metodologias completamente estocásticas orientadas à identificação ARIMA.", "is_correct": True, "specific_explanation": "O documento assinala enfaticamente: 'A metodologia SEATS – ARIMA utiliza metodologia estocástica para identificar sazonalidade e tendência'."},
            {"text": "Uma abordagem pautada puramente em filtros de Suavização Exponencial Simples sem amortecimento.", "is_correct": False, "specific_explanation": "SEATS não é fundamentado na metodologia de suavização SEL Simples."},
            {"text": "O uso irrestrito de extrapolação determinística de múltiplas variáveis dummies sem ponderação.", "is_correct": False, "specific_explanation": "A Decomposição SEATS não utiliza extrapolação determinística como base de identificação dos sinais."},
            {"text": "A aplicação de técnicas de inteligência artificial de aprendizado supervisionado não-linear.", "is_correct": False, "specific_explanation": "Ambos os métodos são ferramentas estatísticas tradicionais de modelagem baseada em ARIMA e médias móveis, sem IA supervisora."}
        ]
    },
    {
        "theme_id": 3,
        "text": "Ao analisar a eficácia na lida com as anomalias temporais da vida real, o que as abordagens combinadas SEATS e X13-ARIMA têm em comum de acordo com a análise de sua capacidade de ajuste?",
        "image_url": None,
        "general_explanation": "Ambas as vertentes avançadas de Decomposição (X13 e SEATS) foram modernizadas para tratar de forma competente anomalias como outliers e para a incorporação inteligente de variáveis exógenas como efeitos de calendário.",
        "concept_slug": "decomposicao-seats-x13",
        "options": [
            {"text": "A capacidade compartilhada de tratar os efeitos de valores extremos (outliers) e de incorporar ativamente os efeitos de calendário nas estimações.", "is_correct": True, "specific_explanation": "A justificação afirma claramente que ambas as metodologias associadas ao ARIMA (X13 e SEATS) tratam os outliers e podem introduzir os efeitos do calendário."},
            {"text": "A limitação de operar de forma exclusivamente aditiva, ignorando a possibilidade de componentes multiplicativos na série de dados reais.", "is_correct": False, "specific_explanation": "As metodologias permitem modelos aditivos, multiplicativos e log-aditivos, não são limitadas à via aditiva."},
            {"text": "A impossibilidade técnica de gerar previsões (forecasts) consistentes sem a intervenção manual do analista para modelar o ruído residual em modelos secundários.", "is_correct": False, "specific_explanation": "Ambas as ferramentas calculam previsões automáticas baseadas em seus ajustes internos otimizados, sem exigência de retrabalho manual para gerar projeções."},
            {"text": "O uso de filtros não adaptativos que homogeneízam o componente sazonal ao longo do tempo independente dos choques estruturais da série.", "is_correct": False, "specific_explanation": "Pelo contrário, elas ajustam dinamicamente a estimativa e permitem mudanças evolutivas nos componentes, tratando justamente choques e quebras por intervenção estocástica."}
        ]
    },
    {
        "theme_id": 3,
        "text": "Por que as estimativas futuras de curto prazo tendem a ser idênticas em ambas metodologias de decomposição (X13 e SEATS) quando as séries possuem um grande número de observações temporais?",
        "image_url": None,
        "general_explanation": "Com o longo período e grande volume de dados, o poder de correção das metodologias estocásticas ARIMA embutidas em ambos os procedimentos conduz as estimativas marginais de previsão à convergência para resultados virtuamente idênticos.",
        "concept_slug": "decomposicao-seats-x13",
        "options": [
            {"text": "Porque o longo histórico permite que as correções estocásticas aplicadas por ambos os métodos convirjam, homogeneizando as projeções futuras em cenários de curto prazo.", "is_correct": True, "specific_explanation": "O gabarito informa explicitamente que com muitas observações, as correções estocásticas feitas longo período tornam as estimativas curtas idênticas."},
            {"text": "Porque no curto prazo os programas do RStudio automaticamente desativam o processamento dos filtros ARIMA por questões de eficiência computacional nas séries longas.", "is_correct": False, "specific_explanation": "O software não desativa metodologias em favor de atalhos em análises rigorosas de decomposição clássica automatizada."},
            {"text": "Devido à premissa do RStudio de substituir qualquer previsão estocástica por uma extrapolação baseada unicamente no intercepto médio de curto prazo independente do método chamado.", "is_correct": False, "specific_explanation": "Não há essa imposição de simplificação arbitrária da extrapolação do intercepto no pacote 'seasonal'."},
            {"text": "Dado o fato de que a sazonalidade desaparece com grandes amostras gerando estacionariedade de longo alcance de forma autônoma para ambos os filtros.", "is_correct": False, "specific_explanation": "A sazonalidade não desaparece, mas as diferenças de modelagem nos filtros se atenuam face à massa de correções estabilizadoras de longo prazo."}
        ]
    },
    {
        "theme_id": 3,
        "text": "No contexto da metodologia de Decomposição estendida (X13-ARIMA / SEATS), o tratamento avançado e modelagem cuidadosa das irregularidades de 'efeitos de calendário' têm como objetivo principal evitar:",
        "image_url": None,
        "general_explanation": "Tratar efeitos de calendário garante que as variações nos feriados flutuantes ou no número de dias úteis sejam adequadamente contabilizadas para não distorcer a extração pura da sazonalidade e da tendência real do fenômeno analisado.",
        "concept_slug": "decomposicao-seats-x13",
        "options": [
            {"text": "A distorção de estimativas sazonais causada pelas flutuações e particularidades das disposições dos dias úteis e feriados ao longo dos anos.", "is_correct": True, "specific_explanation": "A referência aos 'efeitos do calendário' é a correção para impactos de feriados, anos bissextos e fins de semana em variáveis econômicas e de fluxo de dados."},
            {"text": "O superajuste de equações matemáticas que modelam os ciclos de negócios superiores a três décadas em análises conjunturais.", "is_correct": False, "specific_explanation": "Esses efeitos são associados a componente cíclica e tendência longa de Kondratiev ou Juglar, não a 'efeitos de calendário' propriamente mensais e diários."},
            {"text": "A despadronização gerada exclusivamente pela quebra de intercepto nos limites exatos dos anos não-bissextos com meses curtos.", "is_correct": False, "specific_explanation": "Embora o ano bissexto seja relevante, a afirmação é restrita e incorreta para justificar como o tratamento macro age em toda sorte de efeito de calendário de modo aditivo e global."},
            {"text": "A conversão forçada de sazonalidade estocástica para métodos de suavização Holt pura, sem amortecimento, ao avaliar efeitos exógenos não anuais.", "is_correct": False, "specific_explanation": "Esta conversão conceitual é absurda dentro dos papéis delimitados à Decomposição do software."}
        ]
    },
    {
        "theme_id": 3,
        "text": "Qual é a associação fundamental que empodera os antigos algoritmos baseados nas médias móveis (como o X11) a atingirem robustez analítica contra as anomalias modernas como os outliers, conforme visto na aula?",
        "image_url": None,
        "general_explanation": "A introdução de modelos estocásticos pré-ajustados, notadamente a incorporação das metodologias ARIMA antes da fase dos filtros sazonais, permitiu ao X11 estabilizar anomalias proeminentes e tratar pontos fora da curva de forma preditiva inteligente (estendendo-se também aos fins de série).",
        "concept_slug": "decomposicao-seats-x13",
        "options": [
            {"text": "A vinculação umbilical e a implementação embutida da metodologia estocástica ARIMA associada aos passos do filtro estatístico.", "is_correct": True, "specific_explanation": "O texto garante que 'quando associado ao ARIMA (metodologia estocástica)', o X11 trata bem outliers e introduz efeitos de calendário com facilidade."},
            {"text": "A capacidade nativa irrestrita do método de Decomposição original de realizar análises visuais adaptativas que descartam pontos extremos pela observação de quebras de inclinação de forma analógica.", "is_correct": False, "specific_explanation": "O X11 original possuía limitações severas que foram justamente sanadas pela incorporação da etapa paramétrica estocástica (ARIMA)."},
            {"text": "A inserção de dummies de forma recursiva simulada pelas equações de previsão exponenciais de Holt que contornam o componente do erro do X11.", "is_correct": False, "specific_explanation": "A base não é o método SEL Holt, mas a modelagem ARIMA."},
            {"text": "A supressão do termo sazonal visando direcionar toda a variância e complexidade estocástica do sinal diretamente para as projeções baseadas no intercepto simples estático de longo prazo.", "is_correct": False, "specific_explanation": "Não há supressão de componente sazonal; o objetivo é depurá-lo e aperfeiçoar o sinal estocástico adjacente."}
        ]
    },
    {
        "theme_id": 3,
        "text": "Comando R: 'seas(serie)'. Este comando padrão aciona internamente qual motor metodológico de estimativa de componentes de séries temporais na interface detalhada na explicação do RStudio?",
        "image_url": None,
        "general_explanation": "A documentação da prova ilustra de maneira didática que a ausência de especificação adicional evoca a base estocástica nativa por excelência do pacote, estimando pelo procedimento SEATS.",
        "concept_slug": "decomposicao-seats-x13",
        "options": [
            {"text": "O método SEATS, priorizando a decomposição estrutural baseada estritamente em extração a partir de componentes modelados via ARIMA.", "is_correct": True, "specific_explanation": "O texto é claro ao dizer que um deles 'foi estimado pelo comando seas(serie), no qual se estima os componentes da série pelo método SEATS'."},
            {"text": "O filtro X11 clássico puro sem suporte a extensões de identificação estocástica ARIMA para controle de anomalias exógenas.", "is_correct": False, "specific_explanation": "O comando para X11 requer a configuração explícita 'seas(serie, \"X11\")', como apresentado no documento."},
            {"text": "A abordagem analítica unificada baseada estritamente em médias móveis exponenciais centralizadas (versão contemporânea SEL) de longo decaimento em tempo contínuo estendido.", "is_correct": False, "specific_explanation": "Trata-se de métodos não paramétricos simples de filtro ou SEL, o que não reflete a engine TRAMO-SEATS evocada pelo comando seas()."},
            {"text": "O sistema automatizado focado apenas em extrapolações lineares condicionadas com múltiplos regimes sem detecção estocástica interna de componentes.", "is_correct": False, "specific_explanation": "Oseas() opera sobre abordagens consolidadas baseadas em ARIMA para extração simultânea de sinal e sazonalidade."}
        ]
    },
    {
        "theme_id": 3,
        "text": "E para que a decomposição acione especificamente as rotinas associadas à metodologia originária de médias móveis no RStudio, qual é o adendo exigido ao invocar a função 'seas' da série em pauta?",
        "image_url": None,
        "general_explanation": "Para utilizar os cálculos apoiados nos filtros empíricos sucessivos do censo americano, o pacote exige a definição estrita da sintaxe que invoca a ramificação do X11 no argumento da função.",
        "concept_slug": "decomposicao-seats-x13",
        "options": [
            {"text": "O uso do argumento especificando o nome da metodologia, como ilustrado no texto pela chamada seas(serie, \"X11\").", "is_correct": True, "specific_explanation": "O comando seas(serie, \"X11\") foi citado explicitamente no enunciado da questão original referindo-se à estimação do X13 baseada em X11."},
            {"text": "A inclusão prévia de variáveis exógenas sazonais no formulário da série declaradas por dummies estocásticas de sazonalidade.", "is_correct": False, "specific_explanation": "Isso seria montagem manual, mas a alteração de motor X11 ocorre por via direta de argumento da string na função."},
            {"text": "A chamada exclusiva ao comando X13_decomp() isoladamente, visto que o pacote original não suporta a função seas agregadora multimetodológica.", "is_correct": False, "specific_explanation": "O pacote utiliza o wrapper seas() com capacidade de seleção interna."},
            {"text": "A definição global paramétrica do modelo determinístico ignorando as rotinas avançadas de suavização do ruído branco na extração inicial de tendência.", "is_correct": False, "specific_explanation": "Essa não é a maneira pela qual se faz a transição sintática entre SEATS e X11 de acordo com o escopo do RStudio delineado pela avaliação."}
        ]
    },
    {
        "theme_id": 3,
        "text": "Considerando o desempenho em previsões idênticas de curto prazo para grandes amostras, que conceito matemático assegura a confiabilidade preditiva de metodologias que em essência são estruturalmente tão distintas (médias móveis versus estimação espectral estocástica) na área de Decomposição de Séries?",
        "image_url": None,
        "general_explanation": "Os métodos convergem em sua confiabilidade e resultados preditivos à frente de forma idêntica devido às intensas correções estocásticas otimizadas propiciadas pelo longo alcance da série histórica atreladas à formulação convergente ARIMA.",
        "concept_slug": "decomposicao-seats-x13",
        "options": [
            {"text": "A grande densidade de correções estocásticas propiciada pelo expressivo número de observações da série longa faz as projeções do ajustamento marginal do ARIMA convirgir os prognósticos independentemente das extrações pretéritas originárias da decomposição no histórico base.", "is_correct": True, "specific_explanation": "A resposta técnica confirma que 'como há um grande número de observações, no curto prazo as estimativas são idênticas [...] porque as correções aplicadas são estocásticas e por um longo período'."},
            {"text": "A característica comum aos dois modelos que simplesmente abandona as estimativas de incerteza estocástica nos instantes finais em prol da adoção irrestrita da extrapolação do intercepto fixo final calculado a posteriori sem influência da cauda marginal.", "is_correct": False, "specific_explanation": "Nenhuma das abordagens substitui sua formulação complexa pela extrapolação simplista no forecast terminal; a convergência se dá no motor preditivo ARIMA ativo associado ao final de amostras gigantes."},
            {"text": "O engessamento intencional e codificado do RStudio para sempre forçar o X11 a emular os resultados preditivos do SEATS numa rotina arbitrária padronizada ignorando cálculos originais quando a série excede mil observações em tempo discreto.", "is_correct": False, "specific_explanation": "Não existe artifício simplório ou hack forçado, e sim uma convergência estatística legítima dos métodos paramétricos adjuntos otimizados assintoticamente."},
            {"text": "A total dissipação natural e completa de quaisquer anomalias e quebras ao longo das décadas, tornando os dados efetivamente perfeitamente sazonais, não influenciando a distinção preditiva das metodologias na cauda terminal de dados sintéticos.", "is_correct": False, "specific_explanation": "As quebras e distúrbios existem e afetam ambas análises, e sua absorção pelas estruturas do ARIMA longo torna os prognósticos convergentes mesmo não descartando empiricamente anomalias extremas históricas passadas."}
        ]
    },
    {
        "theme_id": 3,
        "text": "A verdadeira ou falsa igualdade preditiva para o futuro de curto prazo entre o X13-ARIMA e o SEATS em longas séries tratadas no ambiente R depende umbilicalmente da modelagem avançada de duas frentes de controle estocástico que os acompanham. Quais sãos estas duas frentes especificadas na prova?",
        "image_url": None,
        "general_explanation": "De forma bastante explícita e repetitiva na resolução, a igualdade ocorre com o suporte contundente de metodologias unificadas e eficientes que garantem a gestão robusta e estocástica no tratamento rigoroso aos outliers severos e a introdução metódica exógena focada nos efeitos indesejados originários do calendário prático contemporâneo.",
        "concept_slug": "decomposicao-seats-x13",
        "options": [
            {"text": "O tratamento acurado dedicado aos outliers e a modelagem incorporada para a introdução minuciosa dos efeitos oriundos das imperfeições de padronização do calendário humano.", "is_correct": True, "specific_explanation": "Ambos métodos ressaltados na defesa teórica citam a capacidade notável estocástica frente aos 'outliers' e aos 'efeitos do calendário' antes de justificar a predição homogênea."},
            {"text": "A identificação estática determinística para tendência exponencial não reativa associada ao bloqueio automático da componente heterocedástica condicionada inerente à volatilidade na estrutura.", "is_correct": False, "specific_explanation": "Os métodos operam ativamente sobre sinais e são responsivos estocásticos, não operam via bloqueio estático e determinístico."},
            {"text": "A desassociação total da série a parâmetros causais externos associada a transformação matemática para a dimensão de log-retornos forçada na extração central contínua.", "is_correct": False, "specific_explanation": "Não há uma desvinculação com premissas base ou transformação rígida global no princípio descritivo avaliado."},
            {"text": "O cálculo analítico retroativo fixo das médias dos anos bissextos e o expurgo contínuo das variações estritamente seculares identificadas por dummies passivas sem componente de viés de intercepto.", "is_correct": False, "specific_explanation": "As médias móveis e a componente estocástica são avançadas, não é expurgo estrito e passivo de dummies em X13 ou SEATS."}
        ]
    }
]

with open(r"c:\Users\paulo.arruda\Desktop\econometria\batch_2.json", "w", encoding="utf-8") as f:
    json.dump(questions, f, indent=2, ensure_ascii=False)

print(f"Generated {len(questions)} questions.")
