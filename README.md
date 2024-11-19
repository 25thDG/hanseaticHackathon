# Hanseatic Hackathon 2024 Base Camp


### Den Basis-Chatbot lokal bauen und ausführen

Um den Basis-Chatbot zu bauen und auszuführen, mache Folgendes:

```
cd chatbot
docker build -t chatbot .
docker run -p 8501:8501 chatbot
```

*Der Container-Build kann einige Zeit dauern, besonders beim ersten Build auf einem Host.*

Jetzt kannst du auf den Chatbot über diesen Link zugreifen [http://localhost:8501](http://localhost:8501).

### Den Prompt Engineering Chatbot lokal bauen und ausführen

Um den Prompt Engineering Chatbot mit Retrieval Augmented Generation zu bauen und auszuführen, mache Folgendes:

```
cd chatbot-rag
docker build --build-arg EMBEDDING_EP=https://bge-m3-embedding.llm.mylab.th-luebeck.dev/ -t chatbot-rag .
docker run -p 8502:8501 chatbot-rag
```

*Der Container-Build kann noch mehr Zeit in Anspruch nehmen, besonders beim ersten Build auf einem Host.*

Jetzt kannst du auf den Chatbot über diesen Link zugreifen [http://localhost:8502](http://localhost:8502).

### Die Kirakatur-Demo lokal bauen und ausführen

Um die Kirakatur-Demo zu bauen und auszuführen, mache Folgendes:

```
cd kirakatur
docker build -t kirakatur .
docker run -p 8503:8501 kirakatur
```

*Der Container-Build kann noch mehr Zeit in Anspruch nehmen, besonders beim ersten Build auf einem Host.*

Jetzt kannst du auf die Kirakatur-Demo über diesen Link zugreifen [http://localhost:8503](http://localhost:8503).

### Deploy

Dieses Repo enthält eine Pipeline, die bereits für automatische Deployments vorbereitet ist. Immer wenn du einen Commit zu diesem Repo machst, wird die Pipeline automatisch gestartet.

Du kannst diesen Prozess jedoch auch manuell auslösen. Starte einfach eine neue [deployment pipeline](../../../-/pipelines/new), um den Beispiel `chatbot` Dienst (ChatBot) bereitzustellen.

***Achtung:** Ein Pipeline-Lauf kann einige Zeit dauern (bis zu 10 Minuten). Die benötigten Bibliotheken umfassen einige Machine Learning-Bibliotheken (pytorch), die nennenswerte Downloadvolumen haben.*

### `kubectl` oder `Lens` konfigurieren

Deine `KUBECONFIG` findest du in Gitlab unter Einstellungen -> [VARIABLES](../../../-/settings/ci_cd).
Kopiere es und importiere es in [Lens](https://k8slens.dev) oder setze es als Umgebungsvariable auf deinem lokalen System.

Du hast dann Zugriff auf deinen verbundenen Kubernetes-Namespace über `kubectl` oder die Lens IDE. Wir empfehlen die Lens IDE.

```bash
kubectl get svc
# Sollte den chatbot, chatbot-rag und kirakatur Dienst zurückgeben
```

```bash
kubectl get pod
# Sollte den chatbot pod, chatbot-rag pod und kirakatur pod zurückgeben
```

Du kannst Serviceports auf dein lokales System weiterleiten mit `kubectl port-forward`

```bash
kubectl port-forward svc/chatbot 8501:8501
kubectl port-forward svc/chatbot-rag 8502:8501
kubectl port-forward svc/kirakatur 8503:8501
```

Jetzt kannst du auf deinen persönlichen ChatBot-Dienst zugreifen:

- [http://localhost:8501](http://localhost:8501): Chatbot
- [http://localhost:8502](http://localhost:8502): Chatbot (Die Version mit der Wissensbasis für Prompt Engineering)
- [http://localhost:8503](http://localhost:8503): Kirakatur-Demo


Du kannst auch die Port-Forwarding-Funktionen von Lens-UI nutzen.

### Deinen Service über einen Ingress der Öffentlichkeit zugänglich machen

Standardmäßig werden deine Services durch das Einrichten eines Ingress öffentlich zugänglich gemacht. Die Pipeline bietet einen manuell ausgelösten Ingress-Job in der Expose-Stufe. Dies macht deinen Service unter folgender extern erreichbarer URL verfügbar:

- `https://chatbot-<< PROJECT_ID >>.llm.mylab.th-luebeck.dev`
- `https://chatbot-rag-<< PROJECT_ID >>.llm.mylab.th-luebeck.dev`
- `https://kirakatur-<< PROJECT_ID >>.llm.mylab.th-luebeck.dev`

Deine Projekt-ID findest du in Gitlab! Wenn du diese README.md in Gitlab (Webbrowser) liest, scrolle einfach ganz nach oben. Du findest die ID im Burgermenü (&vellip;) neben dem Fork-Menü dieses Repos.

Außerdem kannst du bei Bedarf weitere Routen zum Ingress hinzufügen und auch das Update auf automatisch setzen, indem du den Eintrag `when: manual` im Ingress-Manifest `deploy/project-ing.yaml` auskommentierst oder das Manifest sonstwie an deine Bedürfnisse anpasst.

Wenn du das nicht möchtest, deaktiviere den Expose-Job in der Pipeline. Und lösche den Ingress über die Lens UI oder über `kubectl`.

```bash
kubectl delete ing/demo
```

