# ----------------------------------------------------------------------------------------- #
#                                   Criando uma API com Rails                               #
# ----------------------------------------------------------------------------------------- #

# Setup Inicial---------------------------------------------------------------------------- #

0 - Crie seu projeto rodando:

rails new campusero_api --api

1 - Acrescente no seu Gemfile:

# Secure password
gem 'bcrypt', '~> 3.1', '>= 3.1.11'
# jwt authentication
gem 'knock', '~> 2.1', '>= 2.1.1'
# Enable cors in API
gem 'rack-cors'
# Protect API
gem 'rack-attack'

2 - Instale as Gems rodando:

bundle install

3 - Crie o banco de dados rodando:

rake db:create db:migrate

# ----------------------------------------------------------------------------------------- #

# Versionando a API ----------------------------------------------------------------------- #

1 – Dentro da pasta controllers crie uma pasta chamada api

2 – Dentro da pasta criada crie uma nova pasta chamada v1

3 – Dentro da pasta criada crie um arquivo chamado api_controller.rb e coloque nele:


module Api::V1

  class ApiController < ApplicationController
    #> Métodos globais
  end

end

# ----------------------------------------------------------------------------------------- #

# Habilitando o CORS ---------------------------------------------------------------------- #

#OBS: Testar cors

1 - Crie um arquivo (ou atualize) chamado cors.rb em config/initializers/ e coloque nele:

Rails.application.config.middleware.insert_before 0, Rack::Cors do
   allow do
     origins '*'
     resource '*',
       headers: :any,
       methods: [:get, :post, :put, :patch, :delete, :options, :head]
   end
end

# ----------------------------------------------------------------------------------------- #

# Configurando o Rack Attack -------------------------------------------------------------- #

1 - Acrescente em config/application:

config.middleware.use Rack::Attack

2 - Crie um arquivo chamado rack_attack.rb no seu config/initializers/ e coloque nele:

class Rack::Attack
   Rack::Attack.cache.store = ActiveSupport::Cache::MemoryStore.new

   # Allow all local traffic
   safelist('allow-localhost') do |req|
      '127.0.0.1' == req.ip || '::1' == req.ip
   end

   # Allow an IP address to make 5 requests every 5 seconds
   throttle('req/ip', limit: 5, period: 5) do |req|
      req.ip
   end
end

# ----------------------------------------------------------------------------------------- #

# Preparando a autenticação --------------------------------------------------------------- #

1 - Crie o model User rodando:

rails g model User name:string email:string password_digest:string admin:boolean

2 - Atualize o banco de dados rodando:

rails db:migrate

3 - Adicione no Model User:

has_secure_password

4 - Rode o generator do knock:

rails generate knock:token_controller user

5 - Crie o initializer do knock rodando:

rails generate knock:install

6 - Vamos colocar o knock no nosso namespace, atualize o config/routes.rb colocando:

Rails.application.routes.draw do
  namespace :api do
    namespace :v1 do
      post 'user_token', to: 'user_token#create'
    end
  end
end

7 - Mova o arquivo app/controllers/user_token_controller.rb para app/controllers/api/v1/user_token_controller.rb e coloque nele:

class Api::V1::UserTokenController < Knock::AuthTokenController
  # >
end

8 - Atualize o controller api colocando:

module Api::V1

  class ApiController < ApplicationController
    include Knock::Authenticable

    #> Métodos globais
  end

end

9 - Pronto \o/

# ----------------------------------------------------------------------------------------- #

# Testando tudo isso----------------------------------------------------------------------- #

1 - Vamos verificar se o APP devolve o jwt

A) - Abra o rails console rodando:

rails c

B) - Para gerar um usuário rode dentro do console (e depois sai dele digitando exit ):

User.create!(name: 'Leonardo Scorza', email: 'contato@onebitcode.com', password: '12345678')

User.create!(name: 'zz', email: 'z@z', password: '12345678')

C) - Primeiro suba o servidor rodando:

rails s

D) - Abra o postman (ou a ferramenta de requests que preferir)

E) - Faça uma request com os seguintes dados:

url: http://localhost:3000/api/v1/user_token
body: {"auth": {"email": "contato@onebitcode.com", "password": "12345678"}}
type: JSON(application/json)
http method: POST

2 - Vamos ver se o APP reconhece o usuário pelo jwt

A) Vamos gerar o controller User rodando:

rails g controller api/v1/users create destroy show

B) Ajuste as rotas substituindo o conteúdo do arquivo config/routes.rb por:

Rails.application.routes.draw do
  namespace :api do
    namespace :v1 do
      post '/users', to: 'users#create'
      put '/users', to: 'users#update'
      delete '/users/:id', to: 'users#destroy'
      get '/users/:id', to: 'users#show'
      post 'user_token', to: 'user_token#create'
    end
  end

end

C) Atualize o conteúdo do controller user colocando:

class Api::V1::UsersController < Api::V1::ApiController
  before_action :authenticate_user
  # >

  def create
  end

  def destroy
  end

  def show
    p "Logged user name: #{current_user.name}"

    user = User.find(params[:id])
    render json: user
  end
end

D) Abra o postman (ou outra ferramenta de request que você prefira)

E) Realize uma request com os seguintes dados:

url: http://localhost:3000/api/v1/users/1
header: key:Authorization value:Bearer {{your jwt token}}
http method: GET

# ----------------------------------------------------------------------------------------- #

# Preparando a autorização ---------------------------------------------------------------- #

1 - Para gerar as regras do CanCanCan rode:

rails g cancan:ability

2 - Coloque o include e o load no controller API:

include CanCan::ControllerAdditions
load_and_authorize_resource

3 - No arquivo app/models/ability.rb coloque:

class Ability
  include CanCan::Ability

  def initialize(user)
    user ||= User.new # guest user (not logged in)
    if user.admin?
      can :manage, :all
    else
      can :read, :all
      can :manage, Event, user_id: user.id
      can :manage, Talk do |t|
        t.user_id == user.id || t.event.user_id == user.id
      end
      can :destroy, Comment do |c|
        c.user_id == user.id || c.commentable.user_id == user.id
      end
      can :create, Comment
      can :manage, TalkUser do |t|
        t.user_id == user.id || t.talk.user_id == user.id
      end
      can :manage, EventUser do |c|
        c.user_id == user.id || c.event.user_id == user.id
      end
      can [:update, :destroy], User, id: user.id
      can :create, User
    end
  end
end


# ----------------------------------------------------------------------------------------- #

# Gerando os models ----------------------------------------------------------------------- #

1 - Para gerar o model Event rode no console:

rails g model Event title:string description:text user:references begin_date:datetime end_date:datetime

2 - Para gerar o model Talk rode no console:

rails g model Talk title:string description:text user:references event:references begin_date:datetime end_date:datetime

3 - Para gerar o model TalkUser rode no console:

rails g model TalkUsers talk:references user:references

4 - Para gerar o model EventUser rode no console:

rails g model EventUsers event:references user:references

5 - Para gerar o model Comment rode no console:

rails g model Comment body:text user:references commentable_id:integer commentable_type:string

6 - Rode no console:

rake db:migrate

# ----------------------------------------------------------------------------------------- #

# Gerando os controllers ------------------------------------------------------------------ #

## Analisar o que é gerado junto com o controller

1 - Para gerar o controller Users rode no console:

rails g controller api/v1/users create destroy show update

2 - Para gerar o controller Events rode no console:

rails g controller api/v1/events index show create update destroy

3 - Para gerar o controller Talks rode no console:

rails g controller api/v1/talks show create update destroy

4 - Para gerar o controller TalkUsers rode no console:

rails g controller api/v1/talk_users index create destroy

5 - Para gerar o controller EventUsers rode no console:

rails g controller api/v1/event_users index create destroy

6 - Para gerar o controller Comments rode no console:

rails g controller api/v1/comments create destroy

# ----------------------------------------------------------------------------------------- #

# Preparando as rotas    ------------------------------------------------------------------ #

1 - Em config/routes.rb coloque:

Rails.application.routes.draw do
  namespace :api do
    namespace :v1 do
      resources :events, only: [:index, :show, :create, :update, :destroy]
      resources :talks, only: [:create, :update, :destroy, :show]
      resources :comments, only: [:create, :destroy]
      resources :event_talks, only: [:show]
      resources :event_users, only: [:create, :index, :destroy]
      resources :talk_users, only: [:create, :index, :destroy]
      resources :users, only: [:create, :update, :destroy, :show]
      post 'user_token', to: 'user_token#create'
    end
  end
end

2 - Pronto \o/

# ----------------------------------------------------------------------------------------- #


# Desenvolvendo nosso Model Event --------------------------------------------------------- #

1 - Coloque em app/models/event.rb o seguinte código:

class Event < ApplicationRecord # >
  belongs_to :user
  has_many :talks, dependent: :destroy
  has_many :event_users, dependent: :destroy
  has_many :users, through: :event_users
  has_many :comments, as: :commentable, dependent: :destroy

  validates :user, :title, :description, :begin_date, :end_date, presence: true
end

2 - Pronto \o/

# ----------------------------------------------------------------------------------------- #

# Desenvolvendo nosso Model User ---------------------------------------------------------- #

1 - Coloque em app/models/event.rb o seguinte código:

class User < ApplicationRecord # >
  has_secure_password
  validates :name, :email, presence: true
  validates :email, uniqueness: true

  has_many :events, dependent: :destroy
  has_many :talks, dependent: :destroy
  has_many :comments, dependent: :destroy
end

2 - Pronto \o/

# ----------------------------------------------------------------------------------------- #

# Desenvolvendo nosso Model Comment ------------------------------------------------------- #

1 - Coloque em app/models/comment.rb o seguinte código:

class Comment < ApplicationRecord # >
  belongs_to :user
  belongs_to :commentable, polymorphic: true
  validates :body, :commentable, presence: true
end


2 - Pronto \o/

# ----------------------------------------------------------------------------------------- #

# Desenvolvendo nosso Model Talk ---------------------------------------------------------- #

1 - Coloque em app/models/talk.rb o seguinte código:

class Talk < ApplicationRecord # >
  belongs_to :user
  belongs_to :event
  has_many :talk_users, dependent: :destroy
  has_many :users, through: :talk_users
  has_many :comments, as: :commentable, dependent: :destroy


  validates :user, :title, :description, :begin_date, :event_id, :end_date, presence: true
end


2 - Pronto \o/

# ----------------------------------------------------------------------------------------- #

# Desenvolvendo nosso Model TalkUsers ----------------------------------------------------- #

1 - Coloque em app/models/talk_users.rb o seguinte código:

class TalkUser < ApplicationRecord # >
  belongs_to :talk
  belongs_to :user

  validates :talk, :user, presence: true
  validates :talk, uniqueness: { scope: :user, message: "A user just can be added one time" }
end


2 - Pronto \o/

# ----------------------------------------------------------------------------------------- #

# Desenvolvendo nosso Model EventUsers ---------------------------------------------------- #

1 - Coloque em app/models/event_users.rb o seguinte código:

class EventUser < ApplicationRecord # >
  belongs_to :event
  belongs_to :user

  validates :user, :event, presence: true
  validates :event, uniqueness: { scope: :user, message: "A user just can be added one time" }
end

2 - Pronto \o/

# ----------------------------------------------------------------------------------------- #

# Capturando os erros do Active Records e Action Controller ------------------------------- #

1 - No seu app/controllers/api/v1/api_controller.rb coloque:

   rescue_from(ActiveRecord::RecordNotFound) do ||
     render(json: {message: 'Not Found'}, status: :not_found)
   end

   rescue_from(ActionController::ParameterMissing) do |parameter_missing_exception|
      render(json: {message: "Required parameter missing: #{parameter_missing_exception.param}"}, status: :bad_request)
   end

# ----------------------------------------------------------------------------------------- #

# Desenvolvendo o controller Users -------------------------------------------------------- #

1 - Coloque em app/controllers/users_controller.rb o seguinte código:

class Api::V1::UsersController < Api::V1::ApiController # >
  before_action :authenticate_user, only: [:destroy]
  before_action :set_user, only: [:destroy]

  def create
    @user = User.new(user_params)

    if @user.save
      render json: @user, status: :created
    else
      render json: @user.errors, status: :unprocessable_entity
    end
  end


  def update
    if @user.update(user_params)
      render json: @user
    else
      render json: @user.errors, status: :unprocessable_entity
    end
  end

  def destroy
    @user.destroy
  end

  def show
    @user = User.find(params[:id])
    render json: @user.as_json(:except => [:password_digest, :admin, :created_at, :updated_at])
  end

  private

    def set_user
      @user = User.find(params[:id])
    end

    def user_params
      params.require(:user).permit(:name, :email, :password)
    end
end

2 - Pronto \o/

# ----------------------------------------------------------------------------------------- #

# Desenvolvendo o controller Events ------------------------------------------------------- #

1 - Coloque em app/controllers/events_controller.rb o seguinte código:

class Api::V1::EventsController < Api::V1::ApiController # >
  before_action :authenticate_user, only: [:create, :destroy, :update, :comment]
  before_action :set_event, only: [:show, :update, :destroy, :comment]

  def index
    @events = Event.all

    render json: @events
  end

  def show
    render json: @event.as_json(include:[:users, :talks, :comments])
  end

  def create
    @event = Event.new(event_params.merge(user: current_user))

    if @event.save
      render json: @event, status: :created
    else
      render json: @event.errors, status: :unprocessable_entity
    end
  end

  def update
    if @event.update(event_params)
      render json: @event
    else
      render json: @event.errors, status: :unprocessable_entity
    end
  end

  def destroy
    @event.destroy
  end

  private

    def set_event
      @event = Event.find(params[:id])
    end

    def event_params
      params.require(:event).permit(:title, :description, :begin_date, :end_date)
    end
end

2 - Pronto \o/

# ----------------------------------------------------------------------------------------- #

# Desenvolvendo o controller Talks -------------------------------------------------------- #

1 - Coloque em app/controllers/talks_controller.rb o seguinte código:

class Api::V1::TalksController < Api::V1::ApiController # >

  before_action :authenticate_user, only: [:create, :destroy, :update]
  before_action :set_talk, only: [:show, :update, :destroy]
  before_action :is_event_owner?, only: :update

  def show
    render json: @talk.as_json(include:[:users, :comments])
  end

  def create
    @talk = Talk.new(talk_params.merge(user: current_user))

    if @talk.save
      render json: @talk, status: :created
    else
      render json: @talk.errors, status: :unprocessable_entity
    end
  end

  def update
    if @talk.update(talk_params)
      render json: @talk
    else
      render json: @talk.errors, status: :unprocessable_entity
    end
  end

  def destroy
    @talk.destroy
  end

  private

    def set_talk
      @talk = Talk.find(params[:id])
    end

    def talk_params
      params.require(:talk).permit(:title, :description, :begin_date, :end_date, :event_id)
    end

    def is_event_owner?
      event = Event.find(talk_params[:event_id])
      unless event.user == current_user
        raise CanCan::AccessDenied.new("Not authorized!")        
      end
    end
end

2 - Pronto \o/

# ----------------------------------------------------------------------------------------- #

# Desenvolvendo o controller Comments ----------------------------------------------------- #

1 - Coloque em app/controllers/comments_controller.rb o seguinte código:

class Api::V1::CommentsController < Api::V1::ApiController # >
  before_action :authenticate_user
  before_action :set_comment, only: [:destroy]

  def create
    @comment = Comment.new(comment_params.merge(user: current_user))

    if @comment.save
      render json: @comment, status: :created
    else
      render json: @comment.errors, status: :unprocessable_entity
    end
  end

  def destroy
    @comment.destroy
  end

  private

    def set_comment
      @comment = Comment.find(params[:id])
    end

    def comment_params
      params.require(:comment).permit(:body, :commentable_id, :commentable_type)
    end
end

2 - Pronto \o/

# ----------------------------------------------------------------------------------------- #

# Desenvolvendo o controller TalkUsers ---------------------------------------------------- #

1 - Coloque em app/controllers/talk_users_controller.rb o seguinte código:

class Api::V1::TalkUsersController < Api::V1::ApiController # >
  before_action :authenticate_user, only: [:create, :destroy]
  before_action :set_talk_user, only: [:destroy]

  def create
    @talk_user = TalkUser.new(talk_user_params)

    if @talk_user.save
      render json: @talk_user, status: :created
    else
      render json: @talk_user.errors, status: :unprocessable_entity
    end
  end

  def destroy
    @talk_user.destroy
  end

  private

    def set_talk_user
      @talk_user = TalkUser.find(params[:id])
    end

    def talk_user_params
      params.require(:talk_user).permit(:talk_id, :user_id)
    end
end

2 - Pronto \o/

# ----------------------------------------------------------------------------------------- #

# Desenvolvendo o controller EventUsers --------------------------------------------------- #

1 - Coloque em app/controllers/event_users_controller.rb o seguinte código:

class Api::V1::EventUsersController < Api::V1::ApiController # >
  before_action :authenticate_user, only: [:create, :destroy]
  before_action :set_event_user, only: [:destroy]

  def create
    @event_user = EventUser.new(event_user_params)

    if @event_user.save
      render json: @event_user, status: :created
    else
      render json: @event_user.errors, status: :unprocessable_entity
    end
  end

  def destroy
    @event_user.destroy
  end

  private

    def set_event_user
      @event_user = EventUser.find(params[:id])
    end

    def event_user_params
      params.require(:event_user).permit(:event_id, :user_id)
    end
end

2 - Pronto \o/

# ----------------------------------------------------------------------------------------- #

# Preprando nosso seeds.rb ---------------------------------------------------------------- #

1 - Coloque em db/seeds.rb o seguinte código:

# Creating a event
e = Event.create(title: 'Campus Party', description: 'Awesome', user: User.last, begin_date: DateTime.now, end_date: DateTime.now + 1.day)
# Creating a talk
t = Talk.create(title: 'Aprenda a criar uma API com Rails hoje', description: 'Awesome \o/', user: User.last, begin_date: DateTime.now, end_date: DateTime.now + 1.day, event: Event.last)
# Comment in event
e.comments << Comment.create(body: 'Awesome party', user: User.first) # >
# Comment in talk
t.comments << Comment.create(body: 'Awesome slides \o/', user: User.first) # >
# Subscribe user in event
e.users << User.first # >
# Subscribe user in talk
t.users << User.first # >


2 - Pronto \o/

# ----------------------------------------------------------------------------------------- #


# Testando tudo isso com o Postman -------------------------------------------------------- #

0 - Abra o postman para realizarmos os testes

1 - Vamos testar o event

A) Testando o index, rode a seguinte requisição:

URL: http://localhost:3000/api/v1/events
PARAMS: Não é necessário
HEADERS: Não é necessário
HTTP METHOD: GET

B) Testando o show, rode a seguinte requisição:

URL: http://localhost:3000/api/v1/events/1
PARAMS: Não é necessário
HEADERS: Não é necessário
HTTP METHOD: GET

C) Testando o create, rode a seguinte requisição:

URL: http://localhost:3000/api/v1/events
PARAMS: {"event": {"title": "Campus Party BR", "description": "Super Event", "begin_date": "2018-02-01T21:42:34", "end_date": "2018-04-01T21:42:34"}}
HEADERS: Autenticação JWT
HTTP METHOD: POST

D) Testando o update, rode a seguinte requisição:

URL: http://localhost:3000/api/v1/events/1
PARAMS: {"event": {"title": "Campus Party BR \o/"}}
HEADERS: Autenticação JWT
HTTP METHOD: PUT

E) Testando o destroy, rode a seguinte requisição:

URL: http://localhost:3000/api/v1/events/1
PARAMS: Não é necessário
HEADERS: Autenticação JWT
HTTP METHOD: PUT

2 - Vamos testar o talk

A) Testando o show, rode a seguinte requisição:

URL: http://localhost:3000/api/v1/talks/1
PARAMS: Não é necessário
HEADERS: Não é necessário
HTTP METHOD: GET

B) Testando o create, rode a seguinte requisição:

URL: http://localhost:3000/api/v1/talks
PARAMS: {"talk": {"event_id": "1", "title": "Crie uma API hoje", "description": "Super Talk", "begin_date": "2018-02-01T21:42:34", "end_date": "2018-04-01T21:42:34"}}
HEADERS: Autenticação JWT
HTTP METHOD: POST

C) Testando o update, rode a seguinte requisição:

URL: http://localhost:3000/api/v1/talks/1
PARAMS: {"talk": {"title": "Super API \o/"}}
HEADERS: Autenticação JWT
HTTP METHOD: PUT

D) Testando o destroy, rode a seguinte requisição:

URL: http://localhost:3000/api/v1/talks/1
PARAMS: Não é necessário
HEADERS: Autenticação JWT
HTTP METHOD: PUT

3 - Vamos testar o comments

A) Testando o create, rode a seguinte requisição:

URL: http://localhost:3000/api/v1/comments
PARAMS: {"comment": {"body": "good event", "commentable_id": 12, "commentable_type": "Event"}}
HEADERS: Autenticação JWT
HTTP METHOD: POST

B) Testando o destroy, rode a seguinte requisição:

URL: http://localhost:3000/api/v1/comments/7
PARAMS: Não é necessário
HEADERS: Autenticação JWT
HTTP METHOD: PUT

4 - Vamos testar o event_users

A) Testando o create, rode a seguinte requisição:

URL: http://localhost:3000/api/v1/event_users
PARAMS: {"event_user": {"event_id": "x", "user_id": "y"}}
HEADERS: Autenticação JWT
HTTP METHOD: POST

B) Testando o destroy, rode a seguinte requisição:

URL: http://localhost:3000/api/v1/event_users/:id
PARAMS: Não é necessário
HEADERS: Autenticação JWT
HTTP METHOD: PUT

5 - Vamos testar o talk_users

A) Testando o create, rode a seguinte requisição:

URL: http://localhost:3000/api/v1/talk_users
PARAMS: {"talk_user": {"talk_id": "x", "user_id": "y"}}
HEADERS: Autenticação JWT
HTTP METHOD: POST

B) Testando o destroy, rode a seguinte requisição:

URL: http://localhost:3000/api/v1/talk_users/:id
PARAMS: Não é necessário
HEADERS: Autenticação JWT
HTTP METHOD: PUT

6 - Vamos testar o users

A) Testando o create, rode a seguinte requisição:

URL: http://localhost:3000/api/v1/users
PARAMS: {"user": {"name": "teste", "email": "teste@teste.com", "password": "12345678"}}
HEADERS: Não é necessário
HTTP METHOD: POST

B) Testando o destroy, rode a seguinte requisição:

URL: http://localhost:3000/api/v1/users/:id
PARAMS: Não é necessário
HEADERS: Autenticação JWT
HTTP METHOD: PUT

C) Testando o show, rode a seguinte requisição:

URL: http://localhost:3000/api/v1/users/:id
PARAMS: Não é necessário
HEADERS: Não é necessário
HTTP METHOD: GET


# ----------------------------------------------------------------------------------------- #



# ----------------------------------------------------------------------------------------- #
#          Slides e códigos disponíveis em: http://onebitcode.com/api_com_rails_hoje        #
#          Códigos no Github em: https://github.com/leonardoscorza/api_rails_campuseiro     #
# ----------------------------------------------------------------------------------------- #
