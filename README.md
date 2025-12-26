# TestTask - Система аутентификации и авторизации

## Описание проекта

Это проект на FastAPI с асинхронной работой с базой данных PostgreSQL, реализующий систему аутентификации и управления доступом.

Проект позволяет:
- Регистрацию и авторизацию пользователей
- Присвоение ролей пользователям
- Назначение прав ролям
- Контроль доступа к ресурсам по ролям и правам

---

## Структура базы данных

### Таблицы

1. **User**
- `id` (PK)
- `email`
- `password_hash`
- `first_name`, `last_name`, `middle_name`
- `is_active`
- `created_at`, `updated_at`
- Связь с ролями: many-to-many через `user_roles`

2. **Role**
- `id` (PK)
- `name`
- `description`
- Связь с пользователями: many-to-many через `user_roles`
- Связь с permissions: many-to-many через `role_permissions`

3. **Permission**
- `id` (PK)
- `action` — что разрешено делать (`read`, `write`)
- `resource_id` (FK → Resource.id)
- Связь с ролями: many-to-many через `role_permissions`
- Связь с ресурсами: many-to-one

4. **Resource**
- `id` (PK)
- `name` — имя ресурса (`profile`, `notes`, `photos`, `panel`)
- Связь с permissions: one-to-many

5. **UserRole**
- `user_id` (FK → User.id)
- `role_id` (FK → Role.id)

6. **RolePermission**
- `role_id` (FK → Role.id)
- `permission_id` (FK → Permission.id)

---

## Примеры 

### Примеры ролей и разрешений

| Роль    | Ресурс | Действия            | 
| ------- | ------ | ------------------- |
| admin   | panel  | write               |
| manager | notes  | read, write         |
| user    | profile| read, write         |

`panel` - панель управления системой прав и ролей
`notes` - условные заметки менеджеров
`profile` - профиль пользователя

## Схема управления доступом (RBAC)

### Сущности:

- User: пользователь системы, может иметь несколько ролей
- Role: роль пользователя, определяет набор разрешений
- Permission: действие, которое можно совершить на ресурсе
- Resource: объект, к которому применяются разрешения
- UserRole: связь пользователей с ролями
- RolePermission: связь ролей с разрешениями

### Связи:

`User <-- UserRole --> Role <-- RolePermission --> Permission --> Resource`

### Логика:

- Пользователь может иметь несколько ролей.
- Роль может иметь несколько разрешений.
- Разрешение привязано к определенному ресурсу и действию.
- Для доступа к ресурсу необходимо, чтобы у пользователя была роль с соответствующим разрешением.

### Пример структуры:

User: John
Roles: admin, manager
Permissions через роли:

admin → panel: write
admin → photos: read
manager → notes: read, write

## Запуск проекта

### Через Docker

`docker-compose up --build` - запуск
`docker-compose down` - завершение

### Через Makefile

`make up_compose` - запуск
`make down_compose` - завершение


