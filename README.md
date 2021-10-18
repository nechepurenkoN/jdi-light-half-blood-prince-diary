# Введение

Данная статья предназначена прежде всего для тех, кто занимается поддержкой JDI Light. К сожалению, на момент написания
этого материала существует мало информации для мэйнтейнеров, а не конечных пользователей. Автоматизаторы приходят и
уходят, знания не передаются. Из-за этого многие проблемы решаются по несколько раз и разными способами, а пул реквесты
в мастер собирают сотни комментариев, релизы задерживаются.

Местами могут быть ошибки/опечатки и неформальный язык, так удобнее начать. Когда этот материал будет закончен, возможно
частично, и прорецензирован ведущими разработчиками, возможен перевод на английский.

# Оглавление

TODO

# Что не используется

В модулях `material-ui`, `vuetify-js` и др. многие фичи JDI Light не используются/игнорируются. Этот раздел
динамический, что-то будет добавляться/удаляться по мере ревью работ.

Изложенное здесь описано в документации, но не все ее внимательно читают.

Перечитайте, пожалуйста, документацию к JDI Light еще раз. Возможно, вы найдете полезную для мэйнтейнеров информацию или
фичи, которые есть в JDI, но не используются/переписываются еще раз в вашем модуле.

## Локаторы

### Использование не UI аннотаций

Если элемент содержит уникальный текст, то можно воспользоваться аннотациями
`@ByText("example")` и `@WithText("example")`, которые эквивалентны аннотациям с
локаторами `".//*/text()[normalize-space(.) = %s]/parent::*"` и
`".//*/text()[contains(normalize-space(.), %s)]/parent::*"`. Возможно, это повысит читаемость вашего кода.

Пожалуйста, изучите список существующих аннотацией
[по ссылке](https://jdi-docs.github.io/jdi-light/#custom-smart-annotation).

### Возможности аннотации UI

Аннотация `@UI` позволяет нам комбинировать *css* и *xpath* локаторы вместе. В случае с *css* нет возможности, например,
поиска по тексту, но, зачастую, с помощью
*css* селекторов можно удобно ограничить область поиска. При переходе от *css* к *xpath* локатор может раздуться. JDI
позволяет использовать преимущества обоих подходов, например:

*Xpath*: `"//div[contains(@class,'btn')]//*[text()='Submit']"`

*JDI locator*: `div.btn['Submit']`

Больше интересных примеров использования 
[**здесь**](https://jdi-docs.github.io/jdi-light/#jdi-locators-simple-as-css-powerful-as-xpath). 
Пожалуйста, изучите этот абзац, возможно, это сэкономит вам время.

# Поддержка фрэймворков

Полезная (или не очень) информация для разработчиков, имплементирующих кастомные элементы для поддержки различных
фрэймворков: **material-ui**, **vuetify-js** и других.

## Описание задачи

В настоящее время существует множество различных HTML/CSS/JS фреймворков, например,
[**bootstrap**](https://bootstrap5.ru/) или [**W3.css**](https://www.w3schools.com/w3css/default.asp). Они предоставляют
собой некоторый набор переопределенных стилей для основных элементов страницы. Помимо визуального оформления, фрэймворк
может предложить собственный способ организации элементов (некоторые правила верстки), так и собственные javascript
обработчики.

Кастомные элементы/стили/обработчики могут не сохранять/нарушать некоторые стандартные инварианты элементов. Рассмотрим
реализацию `checkbox`, соответствующую стандарту *HTML 5* и реализацию в фрэймворке *material-ui*.

HTML5:

| Unchecked | Checked |
| --- | --- |
| ![html5-unchecked](images/html5-checkbox-unchecked.png) | ![html5-checked](images/html5-checkbox-checked.png) |

В инспекторе нет никаких изменений. Встроенная в JDI Light проверка выглядит следующим образом:

```java
    protected boolean selected() {
        if (getWebElement().isSelected())
            return true;
        return hasClass("checked") || hasClass("active") ||
            hasClass("selected") || attr("checked").equals("true");
    }
```

и она корректно работает для приведенного элемента.

Рассмотрим checkbox в *material-ui*.

Material UI:

| Unchecked | Checked |
| --- | --- |
| ![material-unchecked](images/material-checkbox-unchecked.png) | ![material-checked](images/material-checkbox-checked.png) |

В данном случае стандартная проверка работает не так, как мы ожидаем, выдавая ошибку первого рода. Необходимо
использовать кастомную проверку.

Можно заметить, что к элементу добавляется класс `Mui-checked`, наличие которого можно использовать при проверке.

**Q. Будет ли такая проверка стабильной?**

**A. Необходимо изучить документацию фрэймворка и проверить гарантии, написав набор тестов.**

## С чего начать

### Задачи

Задачи оформляются с помощью [**issue**](https://github.com/jdi-testing/jdi-light/issues).

![Пример issue](images/issue-example.png)

В ней обычно приводится краткое описание задачи, шаги для решения, ссылка на epic (более глобальная задача), ссылки на
пул реквесты или комментарии. Если вы не можете разобраться с формулировкой задачи, проконсультируйтесь с тимлидом.

Статус задачи можно посмотреть на [**доске**](https://github.com/orgs/jdi-testing/projects/1). Пожалуйста, **не
забывайте обновлять** статус задач (In progress, Waiting for demo).

![Пример доски](images/board-columns-example.png)

Задачи можно фильтровать по лэйблу, на рисунке выше выбраны задачи, относящиеся к фрэймворку **vuetify**.

### Стратегия ветвления и оформление пул реквестов

У каждого модуля для поддержки фрэймворка есть **рабочая ветка**, например, `master_material_ui` или `vuetify-develop`.
При выполнении задачи создавайте ветку для нее **из рабочей**.

Правило именование ветки следующее: **[issue-number]-[issue-short-description]**. Пример: 3134-implement-cards,
3281-fix-unused-imports.

Таким образом, всегда можно найти ветку(-и), где происходит разработка. Ваши коллеги могут сделать fetch ветки (IDE
подскажет, когда вы наберете номер issue) и помочь вам в случае проблем/вопросов.

Когда вы закончите выполнение задачи, создайте пул реквест **в рабочую ветку** (не в мастер).

Рассмотрим пример оформления пул реквеста

![Пример пул реквеста](images/pull-request-example.png)

Обратите внимание на название реквеста -- оно должно быть осмысленным. В комментарии желательно описать, что вы сделали,
какие проблемы решили или просто оставить информацию, которую важно знать коллегам/ревьюверу.

Добавьте в *reviewers* **LightReviewTeam**, либо вашего тимлида **(важно!)**.

Сделайте *assign* на себя. Если для вашей задачи предусмотрен *label* -- добавьте его, так будет проще фильтровать пул
реквесты.

Укажите в *projects* доску (см. выше).

Укажите в *linked issues* задачу(-и), которую вы решили.

В совокупности это позволит привязать задачу, пул реквест, ветку к доске и получить результат на рисунке выше.

Пожалуйста, придерживайтесь этих правил.

### Работа с документацией

TODO

Перечитайте [**
гайд**](https://epam-my.sharepoint.com/:w:/p/evgenii_liashenko/Ef5Y3JcicTlPtMmtHg_19T8BLDZqSkBEa7oOgyDxq_hgUA?e=TUcIPI)
для новоприбывших коллег. Пока он не полностью сюда перенесен.

## Реализация кастомных элементов

### Когда нужны или не нужны кастомные элементы

Как "правило большого пальца" используйте следующий чек-лист:

- **Не имплементировать** элементы вида **секции** (неопределенного количества и состава элементов). Можно сделать
  type-alias, если считаете это нужным.
- Имплементируем **значимые** для пользователя элементы.
- Если подобный элемент уже есть в html elements наследуемся от этого элемента.
  **Не изобретайте велосипед**. Переопредление возможно в случаях если реализация элемента во фрэймворке значительно
  отличается и не может быть (совсем или корректно) покрыта существующими решениями.
- Имплементируем элементы по возможности **просто**. Элемент должен быть **переиспользуемым**, не покрывайте слишком
  узкоспециализированную логику.
- В элементах не может быть айдишников или **специфичных для тестового случая** данных.
  **Исключение**: данные, гарантированные фреймворком. Например, в документации указано, что какой-то элемент всегда
  имеет определенный класс.
- **В библиотеке** не может быть **частных случаев** с нашего тестового сайта. Это тестовая верстка, она может повторять
  верстку элементов из документации, но это не дает никаких гарантий (см. выше).

Если у вас есть сомнения - проконсультируйтесь с тимлидом или с человеком, создавшим задачу.

Когда вы создайте класс для элемента, пожалуйста, **указывайте ссылку** на страницу с документацией. Пример:

```java
/**
 * To see an example of Badge web element please visit https://vuetifyjs.com/en/components/badges/
 */
public class Badge extends UIBaseElement<BadgeAssert> {
```

### Написание элемента

Перед написанием собственного элемента необходимо ответить на следующие вопросы:

- **Нужно ли** реализовывать элемент? Чем отличаются существующие решения и **насколько это критично**. (см. п. "Когда
  нужны или не нужны кастомные элементы")
- Определить **тип** элемента: *common*, *complex* или *composite*. Типы описаны в документации [**
  здесь**](https://jdi-docs.github.io/jdi-light/?java#ui-elements-on-contact-form).
- Определить **семантику** элемента: самостоятельный элемент, список или другое. От этого зависит расширяемый класс,
  скорее всего это будут `UIBaseElement<A>` или `UIListBase<A>`. Подробнее они описаны в разделах ниже.
- Выбрать используемые интерфейсы для расширения функционала.
- Определить, подойдут ли **стандартные ассерты**, либо нужно писать **кастомный**. Подробнее при ассерты в разделах
  ниже.

### Обзор UIElement и его иерархии

Иерархия базовых элементов JDI имеет следующий вид:

![Иерархия элементов](images/jdi-element.png)

Скорее всего вам не придется изменять этот код, но неплохо будет понимать, за что отвечает каждый класс и интерфейс.

#### Интерфейс JDIElement

Нужен для получения имени элемента для использования в глобальной Map.

#### Класс DriverBase

Позволяет получить экземпляр драйвера с помощью `driver()`, `JavascriptExecutor` с помощью `js()`.
Предоставляет возможность работать с именем элемента, его родительскими элементами.

Класс `WebPage` не отмечен на диаграмме классов, так как не относится к `UIElement`.
`WebPage` расширяет `DriverBase`.

#### Интерфейс IBaseElement

Позволяет работать с таймаутами, кэшем и предоставляет интерфейс инициализации элемента, имплементирующего его.

#### Класс JDIBase

Определяет правила поиска элемента, работы с локаторами.
Хранит в себе кэш-обертку с `WebElement` и некоторую дополнительную информацию.

#### Интерфейс WebElement

Селениумовский интерфейс, ни больше ни меньше.

#### Интерфейс HasAssert\<A>

Позволяет получить Assertion object элемента.
Дженерик тип `A` нужен для понижающего приведения, подробнее о дженериках в следующих разделах.

Интерфейс предоставляет несколько alias-методов, для повышения читаемости кода.

```java
/**
 * Created by Roman Iovlev on 14.02.2018
 * Email: roman.iovlev.jdi@gmail.com; Skype: roman.iovlev
 */
public interface HasAssert<A> {
    A is();
    default A assertThat() {
        return is();
    }
    default A has() {
        return is();
    }
    default A waitFor() {
        return is();
    }
    default A waitFor(int sec) {
        ((IBaseElement)this).waitSec(sec);
        return is();
    }
    default A shouldBe() {
        return is();
    }
    default A verify() {
        assertSoft(); return is();
    }
}
```

#### Класс UIElement
ы


### Обзор UIBaseElement и прикладных классов

Для реализации кастомных элементов скорее всего будет достаточно расширить классы
`UIBaseElement` или `UIListBase`.

![UIBase](images/uibase.png)

Эти классы содержат в себе экземпляр, вернее `ThreadLocal` подобную обертку над `UIElement`, рассмотренным выше.

В `UIBaseElement` переопределен метод `core()`, возвращающий `UIElement` из этой обертки. Благодаря этому встроенные
интерфейсы с `default` методами могут обращаться к экземпляру. Это удобно тем, что можно при определении класса добавить
интерфейс, например, `IsInput` и его функционал станет доступным без необходимости писать дополнительный код.

### Частые ошибки

TODO

### Написание complex элемента со своими аннотациями

TODO

# Краткий обзор магии JDI

Некоторые особенности внутреннего устройства JDI, которые дадут вам поверхностное понимание того, что происходит под
капотом.

Цель раздела -- мотивировать вас не бояться использовать JDI, потому что это действительно крутой фрэймворк.

Сей раздел есть результат моего субъективного изучения кода и может содержать как неточности, так и серьезные
фактические ошибки. Если вы заметили оное, пожалуйста, исправьте.

## Зачем пересобирать модуль(-и)

При работе с JDI Light очень часто оказывается, что написанный вами код может не логировать определенные действия, не
дожидаться видимости элементов или вовсе падать со `StaleElementException`.

В этом разделе разберемся, как JDI Light позволяет избежать большинства ночных кошмаров/головных болей автоматизаторов и
причем тут пересборка проекта.

### Аспектно-ориентированное программирование

Чтобы понять как работают некоторые фичи JDI Light, необходимо разобраться с АОП. Основные понятия есть
[**на википедии**](https://ru.wikipedia.org/wiki/%D0%90%D1%81%D0%BF%D0%B5%D0%BA%D1%82%D0%BD%D0%BE-%D0%BE%D1%80%D0%B8%D0%B5%D0%BD%D1%82%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%BD%D0%BE%D0%B5_%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5), 
также есть несколько интересных статей на Хабре.

Аспектно-ориентированное программирование позволяет разделять бизнес-логику и некоторую "сопровождающую" логику.
Классические примеры: логирование, транзакционность, фильтрация и другие.

В нашем случае достаточно понимать следующее: мы можем **перехватывать** некоторые действия (например, вызовы методов на
элементе) **и выполнять** некоторый код (до, после, вместо).

Преимущество использования АОП заключается в том, что веб-элементы и "сопровождающая" логика находятся в разных частях и
практически не знают друг о друге. Это позволяет писать обобщенный и хорошо поддерживаемый код.

### Принципы реализации АОП

В основе АОП лежит паттерн проектирования [**прокси**](https://refactoring.guru/design-patterns/proxy). Существует
несколько способов реализации проксирования объектов и инструментов, позволяющих это сделать, остановимся на *AspectJ*.
Этот инструмент позволяет использовать несколько вариантов проксирования объектов: времени компиляции, времени
исполнения. Привожу выдержку [**из
книги**](https://livebook.manning.com/book/aspectj-in-action-second-edition/chapter-8/3) по *AspectJ*:
> The most basic form of weaving is build-time source-code weaving, where the AspectJ compiler compiles source files to produce a woven system. Although this form offers the best experience by providing immediate feedback for source-code errors and by eliminating deployment modifications, using a new compiler can impede AOP adoption. One alternative is build-time byte-code weaving, which lets you delay the introduction of the special compiler until after you compile the code. It also offers a way to weave even when you don’t have access to the source code for classes or aspects. Load-time weaving goes further by eliminating the weaving step from the build process. Instead, it weaves classes as they’re loaded into the VM. Load-time weaving is often the first choice for AspectJ-based tools that want to add new functionality in a minimally invasive fashion. All these choices make adoption of AspectJ easier than ever before.

JDI Light использует компилятор *ajc*, позволяющий встраивать код аспектов в методы элементов (проксировать эти вызовы).
Вы можете заметить это по характерным логам при сборке модулей:

```
[INFO] --- aspectj-maven-plugin:1.12.6:compile (default) @ jdi-light-vuetify ---
[INFO] Showing AJC message detail for messages of types: [error, warning, fail]
[INFO] Join point 'method-call(boolean com.epam.jdi.light.vuetify.elements.complex.Autocomplete.isExpanded())' in Type 'com.epam.jdi.light.vuetify.asserts.AutocompleteAssert' (AutocompleteAssert.java:19) advised by around advice from 'com.epam.jdi.light.vuetify.actions.VuetifyActions' (VuetifyActions.java:31)
[INFO] Join point 'method-execution(com.epam.jdi.light.vuetify.asserts.AutocompleteAssert com.epam.jdi.light.vuetify.asserts.AutocompleteAssert.expanded())' in Type 'com.epam.jdi.light.vuetify.asserts.AutocompleteAssert' (AutocompleteAssert.java:16) advised by around advice from 'com.epam.jdi.light.vuetify.actions.VuetifyActions' (VuetifyActions.java:31)
[INFO] Join point 'method-call(boolean com.epam.jdi.light.vuetify.elements.complex.Autocomplete.isExpanded())' in Type 'com.epam.jdi.light.vuetify.asserts.AutocompleteAssert' (AutocompleteAssert.java:27) advised by around advice from 'com.epam.jdi.light.vuetify.actions.VuetifyActions' (VuetifyActions.java:31)
...
```

Таким образом, для поддержания работы логирования, ожидания и прочего, **необходимо перекомпилировать** тот модуль, в
который вы добавили свой кастомный класс.

Известна проблема, что дефолтные конфигурации запуска в IntelliJ Idea Community Edition (например когда запускаете код
через кнопку Play левее строк с кодом) игнорируют *ajc* и аспектный код не встраивается, что приводит к неправильному
поведению кода. Необходимо изучить проблему и обновить эту часть раздела.

### Аспекты в JDI Light

Рассмотрим пакет `com.epam.jdi.light.actions` в модуле JDI Light.

Условной "точкой входа" является `ActionProcessor`

```java
@Aspect
public class ActionProcessor {
    @Pointcut("within(com.epam.jdi.light..*) && @annotation(com.epam.jdi.light.common.JDIAction)")
    protected void jdiPointcut() {  }
    @Pointcut("execution(* *(..)) && @annotation(io.qameta.allure.Step)")
    protected void stepPointcut() {  }
    @Pointcut("execution(* *(..)) && @annotation(com.epam.jdi.light.common.JDebug)")
    protected void debugPointcut() {  }
    ...
}
```

Здесь видим 3 точки соединения, каждая имеет собственный скоуп. Условие внутри аннотации -- **pointcut designator**,
правила по которым выбираются методы для перехвата. Описание этих правил можно найти в интернете.

Рассмотрим `jdiPointcut`

```java
@Around("jdiPointcut()")
    public Object jdiAround(ProceedingJoinPoint jp) {
        String classMethod = "";
        try {
            classMethod = getJpClass(jp).getSimpleName() + "." + getMethodName(jp);
            logger.trace("<>@AO: " + classMethod);
        } catch (Exception ignore) { }
        ActionObject jInfo = newInfo(jp, "AO");
        failedMethods.clear();
        try {
            BEFORE_JDI_ACTION.execute(jInfo);
            Object result = isTop.get()
                ? stableAction(jInfo)
                : defaultAction(jInfo);
            logger.trace("<>@AO: %s >>> %s",classMethod, (result == null ? "NO RESULT" : result));
            AFTER_JDI_ACTION.execute(jInfo, result);
            return result;
        } catch (Throwable ex) {
            logger.debug("<>@AO exception:" + safeException(ex));
            throw ACTION_FAILED.execute(jInfo, ex);
        }
        finally {
            if (jInfo != null)
                jInfo.clear();
        }
    }
```

Метод `jdiAround` перехватит вызовы методов, аннотированные `@JDIAction`. Аргумент `ProceedingJoinPoint jp` -- содержит
информацию о вызове метода. С помощью utility-метода `newInfo` из `ActionHelper` получаем `ActionObject`, обертку над
перехваченными вызовами, позволяющую работать с `ProceedingJoinPoint` и `JoinPoint`, разница между которыми описана
[**здесь**](https://stackoverflow.com/questions/15781322/joinpoint-vs-proceedingjoinpoint-in-aop-using-aspectj).

`ActionObject` позволяет инкапсулировать логику работы с перехваченными вызовами, некоторые проверки, настройки
таймаутов, получение объекта, у которого вызвали метод и прочее.

Основная логика сосредоточена во втором try-блоке

```java
try {
  BEFORE_JDI_ACTION.execute(jInfo);
  Object result = isTop.get()
      ? stableAction(jInfo)
      : defaultAction(jInfo);
  AFTER_JDI_ACTION.execute(jInfo, result);
  return result;
} catch (Throwable ex) {
    throw ACTION_FAILED.execute(jInfo, ex);
}
```

И здесь можно обнаружить, что есть инструкции до вызова, после, также фабричный метод для исключения и некоторая логика
выполнения метода.

`BEFORE_JDI_ACTION` и `AFTER_JDI_ACTION` предназначены в основном для логирования и *allure*. Результат вызова
перехваченного метода получается либо с помощью `stableAction`, либо `defaultAction` методов.

### Реализация ожиданий

Как раз в `stableAction` реализована логика ожидания с повторением действия при неудаче.

```java
do {
  try {
      logger.trace("do-while: " + getClassMethodName(jInfo.jp()));
      Object result = jInfo.overrideAction() != null
              ? jInfo.overrideAction().execute(jInfo.object()) : jInfo.execute();
      if (!condition(jInfo.jp())) continue;
      return result;
  } catch (Throwable ex) {
      exception = ex;
      try {
          exceptionMsg = safeException(ex);
          Thread.sleep(200);
      } catch (Throwable ignore) {
      }
  }
} while (currentTimeMillis() - start < jInfo.timeout() * 1000L);
throw exception(exception, getFailedMessage(jInfo, exceptionMsg));
```

Заметим, что существует возможность добавить собственные обработчики в `overrideAction()`, с помощью `ActionOverride`.
Также есть `Map` с условиями, при несоблюдении которых результат не будет возвращен и будет произведена еще одна попытка.
```java
    public static MapArray<String, JFunc1<Object, Boolean>> CONDITIONS = map(
            $("", result -> true),
            $("true", result -> result instanceof Boolean && (Boolean) result),
            $("false", result -> result instanceof Boolean && !(Boolean) result),
            $("not empty", result -> result instanceof List && ((List) result).size() > 0),
            $("empty", result -> result instanceof List && ((List) result).size() == 0)
    );
```

### Выводы
Резюмируем выводы по разделу:
1. В JDI Light используется АОП с AspectJ.
2. Поддержка логирования, ожиданий, allure, многопоточности происходит за счет аспектов.
3. Грубо на примере это работает примерно так:

| Было | Стало |
| ---  | --- |
| 1.el.click() | 1. Логи, allure, многопоточность <br>2.Попытка el.click()<br>3.Если неудача goto 2<br>4.Логи, allure, обработка ошибок|
5. Чтобы все заработало, после изменений перекомпилируйте модуль.

Изучение классов и их методов в пакете `com.epam.jdi.light.actions` даст вам более четкое понимание работы JDI Light.

## Обзор JDI Lightsaber

TODO

## Работа с драйвером

TODO

## Поддержка многопоточности

TODO
